import os

base_dir = os.path.abspath(os.path.dirname(__file__))
sqlite_local_base = "sqlite:///user.db"
postgres_local_base = 'postgresql://postgres:123456@localhost/'
database_name = 'api'


class BaseConfig:
    """
    Base application configuration
    """
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_strong_key')
    BCRYPT_HASH_PREFIX = 14
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTH_TOKEN_EXPIRY_DAYS = 30
    AUTH_TOKEN_EXPIRY_SECONDS = 3000


class DevelopmentConfig(BaseConfig):
    """
    Development application configuration
    """
    DEBUG = True
    SECRET_KEY="powerful secretkey"
    SQLALCHEMY_DATABASE_URI=sqlite_local_base


class TestingConfig(BaseConfig):
    """
    Testing application configuration
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_TEST', postgres_local_base + database_name + "_test")
    AUTH_TOKEN_EXPIRY_DAYS = 0
    AUTH_TOKEN_EXPIRY_SECONDS = 3
    AUTH_TOKEN_EXPIRATION_TIME_DURING_TESTS = 5


class ProductionConfig(BaseConfig):
    """
    Production application configuration
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', postgres_local_base + database_name)
    AUTH_TOKEN_EXPIRY_DAYS = 30
    AUTH_TOKEN_EXPIRY_SECONDS = 20

