import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'email-marketing-funnel-secret-key-2024'
    
    # SQLite for easy local run (default). Switch to MySQL by setting DATABASE_URL
    # MySQL example: mysql+pymysql://user:password@localhost:3306/email_marketing
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///email_marketing.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # App settings
    APP_NAME = "Email Marketing Automation Funnel"
    ADMIN_EMAIL = "admin@emailfunnel.com"
