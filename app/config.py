import os
from datetime import timedelta

class Config:
    """Configuration class for the application"""

    # Database configuration
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///blacklist.db')

    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET', 'dev-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    # Static Bearer token for authentication
    APP_ALLOWED_BEARER = os.environ.get('APP_ALLOWED_BEARER', 'dev-bearer-token')

    # Flask configuration
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'
    PORT = int(os.environ.get('PORT', 5000))

    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

    # New Relic configuration
    NEW_RELIC_LICENSE_KEY = os.environ.get('NEW_RELIC_LICENSE_KEY', '01591B20C0FFADDA87E9C64F9CDD2B757B123ACD84F77EE29BAF5D3FA06B256A')
    NEW_RELIC_APP_NAME = os.environ.get('NEW_RELIC_APP_NAME', 'Blacklist Microservice')
