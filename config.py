import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'agrisense-dev-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'agrisense.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    MODEL_PATH = os.path.join(BASE_DIR, 'models', 'crop_disease_model.pth')

    # Disease classes from PlantVillage dataset
    DISEASE_CLASSES = [
        'Apple___Apple_scab',
        'Apple___Black_rot',
        'Apple___Cedar_apple_rust',
        'Apple___healthy',
        'Corn___Cercospora_leaf_spot',
        'Corn___Common_rust',
        'Corn___Northern_Leaf_Blight',
        'Corn___healthy',
        'Grape___Black_rot',
        'Grape___Esca_(Black_Measles)',
        'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
        'Grape___healthy',
        'Potato___Early_blight',
        'Potato___Late_blight',
        'Potato___healthy',
        'Rice___Brown_spot',
        'Rice___Leaf_blast',
        'Rice___Neck_blast',
        'Rice___healthy',
        'Tomato___Bacterial_spot',
        'Tomato___Early_blight',
        'Tomato___Late_blight',
        'Tomato___Leaf_Mold',
        'Tomato___Septoria_leaf_spot',
        'Tomato___Spider_mites',
        'Tomato___Target_Spot',
        'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
        'Tomato___Tomato_mosaic_virus',
        'Tomato___healthy',
        'Wheat___Brown_rust',
        'Wheat___Yellow_rust',
        'Wheat___healthy',
    ]

    NUM_CLASSES = len(DISEASE_CLASSES)
