# AgriSense — AI-Powered Crop Disease Detection & Management System

**Smart India Hackathon 2022 · Problem Statement SG426**  
*Ministry of Agriculture & Farmers' Welfare*

---

## Overview

AgriSense is an end-to-end AI system that detects crop diseases from leaf images and provides actionable treatment recommendations for farmers. Built using deep learning (EfficientNet-B0 with transfer learning), it identifies **32 disease classes across 7 major crops** with high accuracy.

### Key Features

- **Image-based Disease Detection** — Upload a leaf photo → instant diagnosis
- **Treatment & Prevention Plans** — Detailed fungicide recommendations, organic alternatives, and cultural practices  
- **Fertilizer Recommendations** — Nutrient management guidance per disease
- **Analytics Dashboard** — Track diagnosis history, crop health trends, and disease frequency
- **REST API** — For integration with mobile apps and IoT devices
- **Severity Assessment** — From none to critical, with visual indicators

### Supported Crops

| Crop | Diseases | Examples |
|------|----------|---------|
| 🍎 Apple | 4 | Apple Scab, Black Rot, Cedar Rust, Healthy |
| 🌽 Corn | 4 | Cercospora, Common Rust, N. Leaf Blight, Healthy |
| 🍇 Grape | 4 | Black Rot, Esca, Isariopsis Leaf Spot, Healthy |
| 🥔 Potato | 3 | Early Blight, Late Blight, Healthy |
| 🌾 Rice | 4 | Brown Spot, Leaf Blast, Neck Blast, Healthy |
| 🍅 Tomato | 10 | Bacterial Spot, Early/Late Blight, Leaf Mold, etc. |
| 🌾 Wheat | 3 | Brown Rust, Yellow Rust, Healthy |

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Deep Learning | PyTorch, EfficientNet-B0, Transfer Learning |
| Backend | Flask, SQLAlchemy, SQLite |
| Frontend | HTML5, CSS3, JavaScript (ES6+) |
| Visualization | Chart.js |
| Image Processing | Pillow, torchvision |
| ML Utilities | NumPy, scikit-learn |

---

## Project Structure

```
AgriSense/
├── app/
│   ├── __init__.py          # Flask app factory with routes
│   ├── classifier.py        # ML model inference class
│   ├── disease_db.py        # Curated disease knowledge base
│   ├── static/
│   │   ├── css/style.css    # Custom design system
│   │   ├── js/main.js       # Client-side interactions
│   │   ├── images/
│   │   └── uploads/         # User-uploaded images
│   └── templates/
│       ├── base.html        # Base layout
│       ├── index.html       # Landing page
│       ├── diagnose.html    # Image upload & diagnosis
│       ├── result.html      # Diagnosis report
│       ├── history.html     # Past diagnoses
│       ├── dashboard.html   # Analytics dashboard
│       └── about.html       # Project & model info
├── train/
│   ├── train_model.py       # Model training pipeline
│   └── evaluate.py          # Model evaluation & metrics
├── models/                  # Saved model weights
├── data/                    # Dataset directory
├── config.py                # Application configuration
├── run.py                   # App entry point
├── requirements.txt         # Python dependencies
└── README.md
```

---

## Setup & Installation

### 1. Clone and Navigate
```bash
cd AgriSense
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python run.py
```
Visit `http://localhost:5000` in your browser.

---

## Training the Model

### Download Dataset
1. Download the [PlantVillage Dataset](https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset) from Kaggle
2. Extract to `data/PlantVillage/`

### Train
```bash
python train/train_model.py \
    --data_dir data/PlantVillage \
    --epochs 25 \
    --batch_size 32 \
    --lr 0.001
```

### Evaluate
```bash
python train/evaluate.py \
    --model_path models/crop_disease_model.pth \
    --data_dir data/PlantVillage
```

---

## Model Architecture

- **Base Model:** EfficientNet-B0 (pre-trained on ImageNet)
- **Transfer Learning:** Frozen early layers (features[:6])
- **Custom Head:**
  - Dropout(0.3) → Linear(1280, 512) → ReLU → BatchNorm
  - Dropout(0.2) → Linear(512, 256) → ReLU → BatchNorm
  - Dropout(0.1) → Linear(256, 32)
- **Training Strategy:**
  - Optimizer: AdamW (weight decay: 1e-4)
  - Loss: CrossEntropy with label smoothing (0.1)
  - Scheduler: Cosine Annealing Warm Restarts
  - Augmentation: Random crops, flips, rotations, color jitter, perspective, erasing

---

## REST API

### Predict Disease
```
POST /api/predict
Content-Type: multipart/form-data
Body: image=<file>
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "crop": "Tomato",
    "disease": "Late Blight",
    "confidence": 96.4,
    "severity": "Critical",
    "is_healthy": false,
    "treatment": ["..."],
    "prevention": ["..."]
  },
  "alternatives": [...]
}
```

---

## Screenshots

The application features:
- A clean, dark-themed landing page with animated hero section
- Drag-and-drop image upload with live preview
- Detailed diagnosis reports with severity badges
- Interactive analytics dashboard with Chart.js visualizations
- Responsive design for all screen sizes

---

## References

1. PlantVillage Dataset — Hughes & Salathé (2015)
2. EfficientNet — Tan & Le (2019), Google Research
3. Transfer Learning for Plant Disease Classification — Mohanty et al. (2016)
4. ICAR Technical Bulletins on Crop Disease Management
5. Indian Council of Agricultural Research — Disease Management Guides

---

## License

This project is developed for academic purposes as part of Smart India Hackathon 2022.
