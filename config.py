import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dogwalker-secret-key-2024-change-in-prod')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://dogwalker_user:dogwalker_pass@localhost:5432/dogwalker_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # MercadoPago
    MP_ACCESS_TOKEN = os.environ.get('MP_ACCESS_TOKEN', '')
    MP_PUBLIC_KEY = os.environ.get('MP_PUBLIC_KEY', '')
    
    # App Settings
    APP_NAME = 'PataWalker'
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@patawalker.com.br')
