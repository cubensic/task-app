import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration."""
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL',
                                            f'sqlite:///{os.path.join(basedir, "instance", "dev.db")}')
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL',
                                           f'sqlite:///{os.path.join(basedir, "instance", "test.db")}')
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    # Use DATABASE_URL which Railway provides, with fallback to SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or os.environ.get('SQLALCHEMY_DATABASE_URI')
    DEBUG = False
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'ERROR')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT', 'true').lower() == 'true'

    @classmethod
    def init_app(cls, app):
        """Initialize production application."""
        import logging
        from logging.handlers import RotatingFileHandler

        # Configure logging to file
        if not cls.LOG_TO_STDOUT:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/tasks_app.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(getattr(logging, cls.LOG_LEVEL))
            app.logger.addHandler(file_handler)

        # Log to stdout
        else:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(getattr(logging, cls.LOG_LEVEL))
            app.logger.addHandler(stream_handler)

        app.logger.setLevel(getattr(logging, cls.LOG_LEVEL))
        app.logger.info('Tasks App startup')

# Configuration dictionary to easily switch between environments
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 