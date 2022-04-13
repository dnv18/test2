import os
from decouple import config

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')
    DEBUG = config('DEBUG', default='False')
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config('DB_ENGINE', default='postgresql'),
        config('DB_USERNAME', default='username'),
        config('DB_PASS', default='pass'),
        config('DB_HOST', default='localhost'),
        config('DB_PORT', default=5432),
        config('DB_NAME', default='db_name')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    BCRYPT_LOG_ROUNDS = 4
    DEBUG = True


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False
