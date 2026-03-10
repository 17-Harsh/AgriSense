"""
AgriSense — Model Evaluation Script
Generates classification reports, confusion matrices, and per-class metrics.

Usage:
    python train/evaluate.py --model_path models/crop_disease_model.pth --data_dir data/PlantVillage
"""

import os
import sys
import argparse
import json

import torch
import numpy as np
from torch.utils.data import DataLoader
from torchvision import transforms, datasets
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_recall_fscore_support,
)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from train.train_model import build_model


def evaluate_model(model_path, data_dir, batch_size=32, output_dir='models'):
    """Run full evaluation on the validation set."""

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Device: {device}')

    # Load checkpoint
    if not os.path.exists(model_path):
        print(f'Error: Model not found at {model_path}')
        sys.exit(1)

    checkpoint = torch.load(model_path, map_location=device)

    if isinstance(checkpoint, dict) and 'class_names' in checkpoint:
        class_names = checkpoint['class_names']
        num_classes = checkpoint['num_classes']
    else:
        dataset = datasets.ImageFolder(data_dir)
        class_names = dataset.classes
        num_classes = len(class_names)

    print(f'Evaluating model with {num_classes} classes')

    # Build and load model
    model = build_model(num_classes, device)
    if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        model.load_state_dict(checkpoint)

    model.eval()

    # Validation transform
    val_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])

    # Load dataset
    dataset = datasets.ImageFolder(data_dir, transform=val_transform)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=4)

    print(f'Evaluating on {len(dataset)} images...\n')

    # Run inference
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for inputs, labels in loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.numpy())

    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)

    # Metrics
    accuracy = accuracy_score(all_labels, all_preds)
    precision, recall, f1, support = precision_recall_fscore_support(
        all_labels, all_preds, average='weighted'
    )

    print(f'{"=" * 60}')
    print(f'  Overall Metrics')
    print(f'{"=" * 60}')
    print(f'  Accuracy:  {accuracy:.4f} ({accuracy * 100:.2f}%)')
    print(f'  Precision: {precision:.4f}')
    print(f'  Recall:    {recall:.4f}')
    print(f'  F1 Score:  {f1:.4f}')
    print(f'{"=" * 60}\n')

    # Per-class report
    report = classification_report(
        all_labels, all_preds,
        target_names=class_names,
        digits=4,
    )
    print('Per-Class Classification Report:')
    print(report)

    # Save results
    os.makedirs(output_dir, exist_ok=True)

    results = {
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1),
        'num_samples': len(all_labels),
        'num_classes': num_classes,
        'per_class_report': classification_report(
            all_labels, all_preds,
            target_names=class_names,
            digits=4,
            output_dict=True,
        ),
    }

    results_path = os.path.join(output_dir, 'evaluation_results.json')
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f'\nResults saved to {results_path}')

    # Confusion matrix
    cm = confusion_matrix(all_labels, all_preds)
    cm_path = os.path.join(output_dir, 'confusion_matrix.npy')
    np.save(cm_path, cm)
    print(f'Confusion matrix saved to {cm_path}')

    return results


def main():
    parser = argparse.ArgumentParser(description='Evaluate AgriSense model')
    parser.add_argument('--model_path', type=str, default='models/crop_disease_model.pth')
    parser.add_argument('--data_dir', type=str, default='data/PlantVillage')
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--output_dir', type=str, default='models')
    args = parser.parse_args()

    evaluate_model(args.model_path, args.data_dir, args.batch_size, args.output_dir)


if __name__ == '__main__':
    main()
