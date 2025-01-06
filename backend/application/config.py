import os
from flask import current_app as app
from datetime import timedelta
import json
from dotenv import load_dotenv




# Load environment variables from .env file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

class Config:
    """Base Configuration"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_DAYS', 1)))
    ENV = os.getenv('ENV', 'production')

class DevelopmentConfig(Config):
    """Development Configuration"""
    DEBUG = True
    TESTING = False
    ENV = "development"
    SQLALCHEMY_TRACK_MODIFICATIONS = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    SECRET_KEY = Config.SECRET_KEY
    SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI
    JWT_SECRET_KEY = Config.JWT_SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = Config.JWT_ACCESS_TOKEN_EXPIRES

class TestingConfig(Config):
    """Testing Configuration"""
    DEBUG = True
    TESTING = True
    ENV = "testing"
    SQLALCHEMY_TRACK_MODIFICATIONS = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    SECRET_KEY = Config.SECRET_KEY
    SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI
    JWT_SECRET_KEY = Config.JWT_SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = Config.JWT_ACCESS_TOKEN_EXPIRES

class ProductionConfig(Config):
    """Production Configuration"""
    DEBUG = True
    TESTING = True
    ENV = "production"
    SQLALCHEMY_TRACK_MODIFICATIONS = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    SECRET_KEY = Config.SECRET_KEY
    SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI
    JWT_SECRET_KEY = Config.JWT_SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = Config.JWT_ACCESS_TOKEN_EXPIRES
