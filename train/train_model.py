"""
AgriSense — Model Training Script
Trains EfficientNet-B0 on the PlantVillage dataset for crop disease classification.

Dataset: PlantVillage Dataset
    - Download from: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
    - Extract into data/PlantVillage/ directory
    - Expected structure:
        data/PlantVillage/
        ├── Apple___Apple_scab/
        │   ├── image001.jpg
        │   ├── image002.jpg
        │   └── ...
        ├── Apple___Black_rot/
        │   └── ...
        └── ...

Usage:
    python train/train_model.py --data_dir data/PlantVillage --epochs 25 --batch_size 32
"""

import os
import sys
import argparse
import time
import json
from datetime import datetime

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts
from torch.utils.data import DataLoader, random_split
from torchvision import transforms, datasets, models
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config


def get_data_transforms():
    """Define training and validation image transforms with augmentation."""

    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(224, scale=(0.7, 1.0)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.3),
        transforms.RandomRotation(degrees=30),
        transforms.ColorJitter(
            brightness=0.3,
            contrast=0.3,
            saturation=0.3,
            hue=0.1,
        ),
        transforms.RandomAffine(
            degrees=0,
            translate=(0.1, 0.1),
            scale=(0.9, 1.1),
        ),
        transforms.RandomPerspective(distortion_scale=0.2, p=0.3),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
        transforms.RandomErasing(p=0.2, scale=(0.02, 0.15)),
    ])

    val_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])

    return train_transform, val_transform


def build_model(num_classes, device):
    """Build EfficientNet-B0 with custom classification head."""

    model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)

    # Freeze early feature layers
    for param in model.features[:6].parameters():
        param.requires_grad = False

    # Custom classifier head
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(in_features, 512),
        nn.ReLU(),
        nn.BatchNorm1d(512),
        nn.Dropout(p=0.2),
        nn.Linear(512, 256),
        nn.ReLU(),
        nn.BatchNorm1d(256),
        nn.Dropout(p=0.1),
        nn.Linear(256, num_classes),
    )

    model = model.to(device)
    return model


def train_one_epoch(model, dataloader, criterion, optimizer, device):
    """Train model for one epoch."""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (inputs, labels) in enumerate(dataloader):
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()

        # Gradient clipping
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

        optimizer.step()

        running_loss += loss.item() * inputs.size(0)
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

        if (batch_idx + 1) % 50 == 0:
            print(f'  Batch [{batch_idx + 1}/{len(dataloader)}] '
                  f'Loss: {loss.item():.4f} '
                  f'Acc: {100. * correct / total:.2f}%')

    epoch_loss = running_loss / total
    epoch_acc = 100. * correct / total
    return epoch_loss, epoch_acc


def validate(model, dataloader, criterion, device):
    """Validate model on validation set."""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for inputs, labels in dataloader:
            inputs, labels = inputs.to(device), labels.to(device)

            outputs = model(inputs)
            loss = criterion(outputs, labels)

            running_loss += loss.item() * inputs.size(0)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    epoch_loss = running_loss / total
    epoch_acc = 100. * correct / total
    return epoch_loss, epoch_acc, np.array(all_preds), np.array(all_labels)


def main():
    parser = argparse.ArgumentParser(description='Train AgriSense Crop Disease Classifier')
    parser.add_argument('--data_dir', type=str, default='data/PlantVillage',
                        help='Path to PlantVillage dataset directory')
    parser.add_argument('--epochs', type=int, default=25,
                        help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=32,
                        help='Training batch size')
    parser.add_argument('--lr', type=float, default=0.001,
                        help='Initial learning rate')
    parser.add_argument('--val_split', type=float, default=0.2,
                        help='Validation split ratio')
    parser.add_argument('--output_dir', type=str, default='models',
                        help='Output directory for model checkpoints')
    parser.add_argument('--resume', type=str, default=None,
                        help='Path to checkpoint to resume from')
    args = parser.parse_args()

    # Setup
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'\n{"=" * 60}')
    print(f'  AgriSense — Crop Disease Classifier Training')
    print(f'{"=" * 60}')
    print(f'  Device:       {device}')
    print(f'  Data:         {args.data_dir}')
    print(f'  Epochs:       {args.epochs}')
    print(f'  Batch Size:   {args.batch_size}')
    print(f'  Learning Rate: {args.lr}')
    print(f'{"=" * 60}\n')

    # Data transforms
    train_transform, val_transform = get_data_transforms()

    # Load full dataset
    if not os.path.exists(args.data_dir):
        print(f'Error: Dataset directory not found: {args.data_dir}')
        print('Please download the PlantVillage dataset from:')
        print('  https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset')
        print(f'Extract it to: {args.data_dir}')
        sys.exit(1)

    full_dataset = datasets.ImageFolder(args.data_dir)
    class_names = full_dataset.classes
    num_classes = len(class_names)

    print(f'Found {len(full_dataset)} images in {num_classes} classes')
    print(f'Classes: {class_names}\n')

    # Split into train and validation
    val_size = int(len(full_dataset) * args.val_split)
    train_size = len(full_dataset) - val_size

    train_dataset, val_dataset = random_split(
        full_dataset,
        [train_size, val_size],
        generator=torch.Generator().manual_seed(42),
    )

    # Apply transforms
    train_dataset.dataset.transform = train_transform
    val_dataset.dataset.transform = val_transform

    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=4,
        pin_memory=True,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=4,
        pin_memory=True,
    )

    print(f'Training samples:   {train_size}')
    print(f'Validation samples: {val_size}\n')

    # Build model
    model = build_model(num_classes, device)

    # Loss function with label smoothing
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)

    # Optimizer — AdamW with weight decay
    optimizer = optim.AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=args.lr,
        weight_decay=1e-4,
    )

    # Learning rate scheduler
    scheduler = CosineAnnealingWarmRestarts(optimizer, T_0=5, T_mult=2)

    # Resume from checkpoint
    start_epoch = 0
    best_acc = 0.0
    if args.resume and os.path.exists(args.resume):
        checkpoint = torch.load(args.resume, map_location=device)
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        start_epoch = checkpoint['epoch'] + 1
        best_acc = checkpoint.get('accuracy', 0.0)
        print(f'Resumed from epoch {start_epoch}, best accuracy: {best_acc:.2f}%\n')

    # Output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Training history
    history = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': [],
    }

    # Training loop
    print('Starting training...\n')
    for epoch in range(start_epoch, args.epochs):
        epoch_start = time.time()

        print(f'Epoch [{epoch + 1}/{args.epochs}]')
        print('-' * 40)

        # Train
        train_loss, train_acc = train_one_epoch(
            model, train_loader, criterion, optimizer, device
        )

        # Validate
        val_loss, val_acc, _, _ = validate(model, val_loader, criterion, device)

        # Update scheduler
        scheduler.step()

        epoch_time = time.time() - epoch_start

        print(f'  Train Loss: {train_loss:.4f}  Train Acc: {train_acc:.2f}%')
        print(f'  Val Loss:   {val_loss:.4f}  Val Acc:   {val_acc:.2f}%')
        print(f'  Time: {epoch_time:.1f}s  LR: {optimizer.param_groups[0]["lr"]:.6f}')

        # Save history
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)

        # Save best model
        if val_acc > best_acc:
            best_acc = val_acc
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'accuracy': val_acc,
                'loss': val_loss,
                'class_names': class_names,
                'num_classes': num_classes,
            }
            model_path = os.path.join(args.output_dir, 'crop_disease_model.pth')
            torch.save(checkpoint, model_path)
            print(f'  ★ Saved best model (accuracy: {best_acc:.2f}%)')

        print()

    # Save training history
    history_path = os.path.join(args.output_dir, 'training_history.json')
    with open(history_path, 'w') as f:
        json.dump(history, f, indent=2)

    # Save class names mapping
    class_map_path = os.path.join(args.output_dir, 'class_names.json')
    with open(class_map_path, 'w') as f:
        json.dump({
            'class_names': class_names,
            'num_classes': num_classes,
            'trained_at': datetime.now().isoformat(),
            'best_accuracy': best_acc,
            'epochs_trained': args.epochs,
        }, f, indent=2)

    print(f'\n{"=" * 60}')
    print(f'  Training Complete!')
    print(f'  Best Validation Accuracy: {best_acc:.2f}%')
    print(f'  Model saved to: {os.path.join(args.output_dir, "crop_disease_model.pth")}')
    print(f'{"=" * 60}\n')


if __name__ == '__main__':
    main()
