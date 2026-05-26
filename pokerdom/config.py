import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-me')
DATABASE_URL= os.environ.get('DATABASE_URL', 'postgresql://poker:poker@localhost:5432/pokerdom')
NVIDIA_API_KEY= os.environ.get('NVIDIA_API_KEY', '')
FLASK_DEBUG= os.environ.get('FLASK_ENV', 'development') == 'development'
PORT= int(os.environ.get('PORT', 5000))
