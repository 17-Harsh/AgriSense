"""
AgriSense — Crop Disease Classifier
Uses EfficientNet-B0 with transfer learning for crop disease classification.
Supports 32 disease classes across 7 major crops.
"""

import os
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import numpy as np


class CropDiseaseClassifier:
    """CNN-based classifier for crop leaf disease detection using EfficientNet-B0."""

    # ImageNet normalization parameters
    IMAGENET_MEAN = [0.485, 0.456, 0.406]
    IMAGENET_STD = [0.229, 0.224, 0.225]
    INPUT_SIZE = 224

    def __init__(self, model_path, class_names, device=None):
        """
        Initialize the classifier.

        Args:
            model_path: Path to saved model weights (.pth file)
            class_names: List of class names corresponding to model outputs
            device: torch device (auto-detected if None)
        """
        self.class_names = class_names
        self.device = device or torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu'
        )
        self.model = self._build_model(len(class_names))
        self.transform = self._build_transform()

        if os.path.exists(model_path):
            self._load_weights(model_path)
        else:
            print(f"[AgriSense] No trained weights found at {model_path}")
            print("[AgriSense] Model initialized with pre-trained ImageNet weights")
            print("[AgriSense] Run train/train_model.py to train on PlantVillage dataset")

        self.model.eval()
        self.model.to(self.device)

    def _build_model(self, num_classes):
        """Build EfficientNet-B0 model with custom classification head."""
        try:
            model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
            print("[AgriSense] Loaded EfficientNet-B0 with ImageNet weights")
        except (RuntimeError, Exception) as e:
            print(f"[AgriSense] Standard weight loading failed: {e}")
            print("[AgriSense] Attempting to load weights with check_hash=False...")
            try:
                model = models.efficientnet_b0(weights=None)
                from torch.hub import load_state_dict_from_url
                EFFICIENTNET_B0_URL = "https://download.pytorch.org/models/efficientnet_b0_rwightman-3dd342df.pth"
                state_dict = load_state_dict_from_url(
                    EFFICIENTNET_B0_URL,
                    progress=True,
                    check_hash=False,
                )
                model.load_state_dict(state_dict)
                print("[AgriSense] Loaded EfficientNet-B0 with ImageNet weights (hash check skipped)")
            except Exception as e2:
                print(f"[AgriSense] Could not load pretrained weights: {e2}")
                model = models.efficientnet_b0(weights=None)

        # Freeze early layers for transfer learning
        for param in model.features[:6].parameters():
            param.requires_grad = False

        # Replace classifier with custom head
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

        return model

    def _build_transform(self):
        """Build image preprocessing pipeline."""
        return transforms.Compose([
            transforms.Resize((self.INPUT_SIZE, self.INPUT_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(mean=self.IMAGENET_MEAN, std=self.IMAGENET_STD),
        ])

    def _load_weights(self, model_path):
        """Load saved model weights."""
        try:
            checkpoint = torch.load(model_path, map_location=self.device)
            if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                self.model.load_state_dict(checkpoint['model_state_dict'])
                print(f"[AgriSense] Loaded model (Epoch {checkpoint.get('epoch', '?')}, "
                      f"Acc: {checkpoint.get('accuracy', '?')})")
            else:
                self.model.load_state_dict(checkpoint)
                print(f"[AgriSense] Loaded model weights from {model_path}")
        except Exception as e:
            print(f"[AgriSense] Error loading weights: {e}")
            print("[AgriSense] Using pre-trained ImageNet weights")

    def _is_valid_leaf(self, image):
        """Check if image has sufficient plant-like color representation."""
        import matplotlib.colors as mcolors
        img_thumb = image.copy()
        img_thumb.thumbnail((150, 150))
        img_np = np.array(img_thumb) / 255.0
        hsv = mcolors.rgb_to_hsv(img_np)
        
        hue = hsv[:,:,0] * 360
        sat = hsv[:,:,1]
        val = hsv[:,:,2]
        
        # Greens, yellows, browns: hues approx 15 to 165
        # Ignore dark pixels or grey pixels
        valid = ((hue >= 15) & (hue <= 165) & (sat >= 0.15) & (val >= 0.15))
        ratio = np.sum(valid) / valid.size
        
        return ratio >= 0.40 # At least 40% plant pixels

    def predict(self, image_path, top_k=3):
        """
        Predict disease from a leaf image.

        Args:
            image_path: Path to the leaf image
            top_k: Number of top predictions to return

        Returns:
            dict with prediction results including class name,
            confidence, and top-k alternatives
        """
        image = Image.open(image_path).convert('RGB')
        
        if not self._is_valid_leaf(image):
            raise ValueError("The uploaded image does not appear to be a crop leaf. Please upload a clear leaf image.")

        input_tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(input_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)

        top_probs, top_indices = torch.topk(probabilities, top_k)
        top_probs = top_probs.squeeze().cpu().numpy()
        top_indices = top_indices.squeeze().cpu().numpy()

        # Handle single prediction case
        if top_probs.ndim == 0:
            top_probs = np.array([top_probs.item()])
            top_indices = np.array([top_indices.item()])

        primary_idx = top_indices[0]
        primary_class = self.class_names[primary_idx]
        primary_confidence = float(top_probs[0])

        # Parse crop and disease from class name
        parts = primary_class.split('___')
        crop_name = parts[0] if len(parts) > 0 else 'Unknown'
        disease_name = parts[1].replace('_', ' ') if len(parts) > 1 else 'Unknown'

        results = {
            'class_key': primary_class,
            'crop': crop_name,
            'disease': disease_name,
            'confidence': primary_confidence,
            'is_healthy': 'healthy' in primary_class.lower(),
            'top_predictions': [],
        }

        for i in range(len(top_probs)):
            idx = top_indices[i]
            cls = self.class_names[idx]
            parts = cls.split('___')
            results['top_predictions'].append({
                'class_key': cls,
                'crop': parts[0] if len(parts) > 0 else 'Unknown',
                'disease': parts[1].replace('_', ' ') if len(parts) > 1 else 'Unknown',
                'confidence': float(top_probs[i]),
            })

        return results

    def get_model_info(self):
        """Return model architecture information."""
        total_params = sum(p.numel() for p in self.model.parameters())
        trainable_params = sum(
            p.numel() for p in self.model.parameters() if p.requires_grad
        )
        return {
            'architecture': 'EfficientNet-B0 (Transfer Learning)',
            'total_parameters': f'{total_params:,}',
            'trainable_parameters': f'{trainable_params:,}',
            'input_size': f'{self.INPUT_SIZE}x{self.INPUT_SIZE}',
            'num_classes': len(self.class_names),
            'device': str(self.device),
        }
