"""
AgriSense Flask Application
"""

import os
import uuid
import json
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from config import Config
from app.classifier import CropDiseaseClassifier
from app.disease_db import DISEASE_INFO

db = SQLAlchemy()

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ─────────────── Database Model ───────────────
# Defined BEFORE create_app so db.create_all() can find it

class DiagnosisRecord(db.Model):
    __tablename__ = 'diagnosis_records'

    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String(255), nullable=False)
    crop = db.Column(db.String(100), nullable=False)
    disease = db.Column(db.String(200), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    severity = db.Column(db.String(50), default='Unknown')
    is_healthy = db.Column(db.Boolean, default=False)
    class_key = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Diagnosis {self.crop}: {self.disease} ({self.confidence:.0%})>'


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)

    # Initialize ML model
    classifier = CropDiseaseClassifier(
        model_path=app.config['MODEL_PATH'],
        class_names=app.config['DISEASE_CLASSES'],
    )

    # Create database tables
    with app.app_context():
        db.create_all()

    # ─────────────────────────── Routes ───────────────────────────

    @app.route('/')
    def index():
        """Landing page."""
        recent_analyses = DiagnosisRecord.query.order_by(
            DiagnosisRecord.created_at.desc()
        ).limit(5).all()
        stats = get_statistics()
        return render_template('index.html', recent=recent_analyses, stats=stats)

    @app.route('/diagnose', methods=['GET', 'POST'])
    def diagnose():
        """Upload and diagnose leaf image."""
        if request.method == 'POST':
            if 'leaf_image' not in request.files:
                flash('No image file selected.', 'error')
                return redirect(request.url)

            file = request.files['leaf_image']
            if file.filename == '':
                flash('No image file selected.', 'error')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                # Save with unique filename
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f'{uuid.uuid4().hex}.{ext}'
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Run prediction
                try:
                    result = classifier.predict(filepath, top_k=3)
                except Exception as e:
                    flash(f'Error analyzing image: {str(e)}', 'error')
                    return redirect(request.url)

                # Get disease information
                disease_info = DISEASE_INFO.get(result['class_key'], {})

                # Determine severity
                severity = disease_info.get('severity', 'Unknown')
                if result['is_healthy']:
                    severity = 'None'

                # Save to database
                record = DiagnosisRecord(
                    image_filename=filename,
                    crop=result['crop'],
                    disease=disease_info.get('disease', result['disease']),
                    confidence=result['confidence'],
                    severity=severity,
                    is_healthy=result['is_healthy'],
                    class_key=result['class_key'],
                )
                db.session.add(record)
                db.session.commit()

                return render_template(
                    'result.html',
                    result=result,
                    disease_info=disease_info,
                    image_filename=filename,
                    record_id=record.id,
                )
            else:
                flash('Invalid file type. Please upload a JPG, PNG, or WebP image.', 'error')
                return redirect(request.url)

        return render_template('diagnose.html')

    @app.route('/history')
    def history():
        """View diagnosis history."""
        page = request.args.get('page', 1, type=int)
        per_page = 12
        records = DiagnosisRecord.query.order_by(
            DiagnosisRecord.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        return render_template('history.html', records=records)

    @app.route('/dashboard')
    def dashboard():
        """Analytics dashboard."""
        stats = get_statistics()
        crop_data = get_crop_distribution()
        severity_data = get_severity_distribution()
        monthly_data = get_monthly_trend()
        disease_frequency = get_disease_frequency()
        return render_template(
            'dashboard.html',
            stats=stats,
            crop_data=json.dumps(crop_data),
            severity_data=json.dumps(severity_data),
            monthly_data=json.dumps(monthly_data),
            disease_frequency=json.dumps(disease_frequency),
        )

    @app.route('/about')
    def about():
        """About page with model information."""
        model_info = classifier.get_model_info()
        return render_template('about.html', model_info=model_info)

    @app.route('/api/predict', methods=['POST'])
    def api_predict():
        """REST API endpoint for predictions."""
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        file = request.files['image']
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400

        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f'{uuid.uuid4().hex}.{ext}'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            result = classifier.predict(filepath, top_k=3)
            disease_info = DISEASE_INFO.get(result['class_key'], {})

            return jsonify({
                'success': True,
                'prediction': {
                    'crop': result['crop'],
                    'disease': disease_info.get('disease', result['disease']),
                    'confidence': round(result['confidence'] * 100, 2),
                    'severity': disease_info.get('severity', 'Unknown'),
                    'is_healthy': result['is_healthy'],
                    'treatment': disease_info.get('treatment', []),
                    'prevention': disease_info.get('prevention', []),
                },
                'alternatives': result['top_predictions'],
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # ─────────────── Helper Functions ───────────────

    def get_statistics():
        total = DiagnosisRecord.query.count()
        diseased = DiagnosisRecord.query.filter_by(is_healthy=False).count()
        healthy = DiagnosisRecord.query.filter_by(is_healthy=True).count()
        crops = db.session.query(DiagnosisRecord.crop).distinct().count()
        avg_conf = db.session.query(
            db.func.avg(DiagnosisRecord.confidence)
        ).scalar() or 0

        return {
            'total_scans': total,
            'diseased': diseased,
            'healthy': healthy,
            'crops_analyzed': crops,
            'avg_confidence': round(float(avg_conf) * 100, 1),
        }

    def get_crop_distribution():
        results = db.session.query(
            DiagnosisRecord.crop,
            db.func.count(DiagnosisRecord.id),
        ).group_by(DiagnosisRecord.crop).all()
        return {
            'labels': [r[0] for r in results],
            'data': [r[1] for r in results],
        }

    def get_severity_distribution():
        results = db.session.query(
            DiagnosisRecord.severity,
            db.func.count(DiagnosisRecord.id),
        ).group_by(DiagnosisRecord.severity).all()
        return {
            'labels': [r[0] for r in results],
            'data': [r[1] for r in results],
        }

    def get_monthly_trend():
        results = db.session.query(
            db.func.strftime('%Y-%m', DiagnosisRecord.created_at),
            db.func.count(DiagnosisRecord.id),
        ).group_by(
            db.func.strftime('%Y-%m', DiagnosisRecord.created_at)
        ).order_by(
            db.func.strftime('%Y-%m', DiagnosisRecord.created_at)
        ).limit(12).all()
        return {
            'labels': [r[0] for r in results],
            'data': [r[1] for r in results],
        }

    def get_disease_frequency():
        results = db.session.query(
            DiagnosisRecord.disease,
            db.func.count(DiagnosisRecord.id),
        ).filter(
            DiagnosisRecord.is_healthy == False  # noqa: E712
        ).group_by(
            DiagnosisRecord.disease
        ).order_by(
            db.func.count(DiagnosisRecord.id).desc()
        ).limit(10).all()
        return {
            'labels': [r[0] for r in results],
            'data': [r[1] for r in results],
        }

    return app
