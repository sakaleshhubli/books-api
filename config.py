import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORITHM = 'HS256'
    
    # File storage settings
    BOOKS_FILE = 'books.json'
    AUTHORS_FILE = 'authors.json'
    USERS_FILE = 'users.json'
    
    # Default data files
    DEFAULT_BOOKS_FILE = 'data/default_books.json'
    DEFAULT_AUTHORS_FILE = 'data/default_authors.json'
    DEFAULT_USERS_FILE = 'data/default_users.json'
    
    # Validation limits
    MAX_TITLE_LENGTH = 200
    MAX_AUTHOR_LENGTH = 100
    MAX_GENRE_LENGTH = 50
    MAX_DESCRIPTION_LENGTH = 1000
    MIN_YEAR = 1800
    MAX_YEAR = datetime.now().year + 1
    
    # User validation limits
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 50
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 128
    MAX_EMAIL_LENGTH = 255
    
    # API settings
    API_TITLE = "Book API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "A RESTful API for managing books and authors with authentication"
    
    # Pagination
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100
    
    # Search settings
    MIN_SEARCH_QUERY_LENGTH = 2
    MAX_SEARCH_QUERY_LENGTH = 100
    
    # Rate limiting
    RATE_LIMIT_ENABLED = True
    RATE_LIMIT_REQUESTS = 100  # requests per hour
    RATE_LIMIT_WINDOW = 3600   # 1 hour in seconds

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # Longer tokens for development

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    RATE_LIMIT_REQUESTS = 1000  # Higher limits for production

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    BOOKS_FILE = 'test_books.json'
    AUTHORS_FILE = 'test_authors.json'
    USERS_FILE = 'test_users.json'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)  # Short tokens for testing

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 