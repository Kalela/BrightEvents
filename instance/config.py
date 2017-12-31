import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')

class DevelopmentConfig(Config):
    """Configurations for Development mode."""
    DEBUG = True

class TestingConfig(Config):
    """Configurations for testing"""
    TESTING = True
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