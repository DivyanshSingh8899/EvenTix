import os

class TestConfig:
    """Test configuration for Flask app"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for testing
    SECRET_KEY = 'test-secret-key-12345'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing
    
class DevelopmentConfig:
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True
    
class ProductionConfig:
    """Production configuration"""
    DEBUG = False
    TESTING = False
