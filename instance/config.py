#Import dependancies
import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = False
    SECRET_KEY = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    MAIL_SERVER=os.getenv('MAIL_SERVER')
    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD') + "$$"
    MAIL_PORT=os.getenv('MAIL_PORT')
    MAIL_USE_SSL=True
    MAIL_USE_TLS=False
    ADMINS = ['brightevents123@gmail.com']

class DevelopmentConfig(Config):
    """Configurations for Development mode."""
    DEBUG = True

class TestingConfig(Config):
    """Configurations for testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://kalela:challenge123@localhost/test_db"
    DEBUG = True

class StagingConfig(Config):
    """Configurations for staging"""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production"""
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
