"""
AgriSense — Crop Disease Classifier
Uses EfficientNet-B0 with transfer learning for crop disease classification.
Supports 32 disease classes across 7 major crops.

Includes an ImageNet-based gatekeeper to reject non-leaf images (stones, forests, etc.)
before the disease model runs.
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

    # ── Plant-related ImageNet category keywords ──
    # If ANY of the ImageNet top-20 predictions contains these keywords,
    # the image is considered to potentially contain plant material.
    # This is intentionally comprehensive and permissive for valid leaves.
    PLANT_KEYWORDS = [
        # Vegetables
        'cabbage', 'broccoli', 'cauliflower', 'zucchini', 'squash',
        'cucumber', 'artichoke', 'pepper', 'cardoon', 'mushroom',
        'pumpkin', 'turnip',
        # Fruits
        'apple', 'granny_smith', 'strawberry', 'orange', 'lemon',
        'fig', 'pineapple', 'banana', 'jackfruit', 'custard_apple',
        'pomegranate',
        # Crops & agricultural
        'hay', 'rapeseed', 'corn', 'ear',  # ear of corn
        'acorn', 'hip', 'buckeye',  # seeds/nuts
        # Flowers
        'daisy', 'sunflower', 'rose', 'tulip', 'orchid', 'poppy',
        'lady_slipper', "yellow_lady",
        # Fungi (relevant since diseases involve fungi)
        'fungus', 'agaric', 'gyromitra', 'stinkhorn', 'earthstar',
        'bolete', 'coral_fungus', 'hen-of-the-woods',
        # Plant-related objects & textures
        'pot', 'flower_pot', 'vase',
        'leaf', 'plant', 'herb', 'vine', 'fern', 'moss',
        'seed', 'sprout', 'blossom', 'petal',
        # Insects commonly found ON leaves (ImageNet classifies leaf
        # close-ups as these because the leaf dominates the image)
        'leaf_beetle', 'beetle', 'leafhopper',
        # Broader nature keywords (close-up plant material)
        'tobacco', 'cocoa', 'coffee',
    ]

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

        # Initialize the ImageNet-based leaf gatekeeper
        self._init_gatekeeper()

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

    # ─────────────── ImageNet Gatekeeper ───────────────

    def _init_gatekeeper(self):
        """
        Initialize a SEPARATE ImageNet EfficientNet-B0 (1000 classes) as a
        leaf/plant detector. This model answers: "Does this image contain
        plant material?" BEFORE the disease classifier runs.
        """
        try:
            weights = models.EfficientNet_B0_Weights.DEFAULT
            self._gatekeeper = models.efficientnet_b0(weights=weights)
            self._gatekeeper.eval()
            self._gatekeeper.to(self.device)
            self._imagenet_categories = weights.meta["categories"]
            self._gatekeeper_ready = True
            print("[AgriSense] Leaf gatekeeper initialized (ImageNet OOD detection)")
        except Exception as e:
            print(f"[AgriSense] WARNING: Leaf gatekeeper failed to load: {e}")
            print("[AgriSense] OOD detection disabled — all images will be processed")
            self._gatekeeper_ready = False

    def _is_plant_category(self, category_name):
        """Check if an ImageNet category name matches any plant-related keyword."""
        cat = category_name.lower().replace(' ', '_').replace("'", '')
        for keyword in self.PLANT_KEYWORDS:
            if keyword.lower() in cat:
                return True
        return False

    def _is_valid_leaf(self, image):
        """
        Validate that the image contains plant/leaf material using the
        ImageNet gatekeeper model.

        Runs the full 1000-class ImageNet EfficientNet-B0. If ANY of the
        top-20 predictions is a plant-related category (cumulative probability
        >= 2%), the image is accepted. Otherwise it is rejected.

        This reliably catches:
        - Stones/rocks → ImageNet says "alp", "cliff", "volcano" → rejected
        - Forests/landscapes → ImageNet says "valley", "lakeside" → rejected
        - Random objects → ImageNet says "window screen", etc. → rejected
        - Valid crop leaves → ImageNet says "leaf beetle", "lady's slipper" → accepted
        """
        if not self._gatekeeper_ready:
            return True  # Skip if gatekeeper not available

        input_tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self._gatekeeper(input_tensor)
            probs = torch.nn.functional.softmax(outputs, dim=1)

        # Check top-20 predictions for any plant-related category
        top_probs, top_indices = torch.topk(probs, 20)
        top_probs = top_probs.squeeze().cpu().numpy()
        top_indices = top_indices.squeeze().cpu().numpy()

        plant_score = 0.0
        for i in range(len(top_indices)):
            category = self._imagenet_categories[top_indices[i]]
            if self._is_plant_category(category):
                plant_score += float(top_probs[i])

        # Accept if at least 2% cumulative probability for plant categories
        return plant_score >= 0.02

    # ─────────────── Prediction ───────────────

    def predict(self, image_path, top_k=3):
        """
        Predict disease from a leaf image.

        Args:
            image_path: Path to the leaf image
            top_k: Number of top predictions to return

        Returns:
            dict with prediction results including class name,
            confidence, and top-k alternatives

        Raises:
            ValueError: If image does not appear to contain a plant/leaf
        """
        image = Image.open(image_path).convert('RGB')

        if not self._is_valid_leaf(image):
            raise ValueError(
                "This image does not appear to contain a crop leaf. "
                "Please upload a clear, close-up photo of a plant leaf for diagnosis."
            )

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
            'ood_detection': 'ImageNet Gatekeeper (1000-class)',
        }

