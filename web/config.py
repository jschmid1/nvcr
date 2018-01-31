import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{passwd}@{host}:{port}/{db}'.format(
            user = os.getenv('DB_USER', 'docker'),
            passwd = os.getenv('DB_PASS', 'docker'),
            host = os.getenv('DB_HOST', 'postgres'),
            port = os.getenv('DB_PORT', '5432'),
            db = os.getenv('DB_NAME', 'docker')
            )
    SECRET_KEY = os.getenv('SECRET_KEY', 'development')
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
