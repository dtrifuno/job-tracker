import os

from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ACCESS_TOKEN_EXPIRES = 120
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TOKEN_PREFIX = "Bearer"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    @staticmethod
    def init_app(app):
        super(DevelopmentConfig, DevelopmentConfig).init_app(app)
        CORS(app=app, origins=[r"^https?://localhost:\d+$", r"^https?://127.0.0.1:\d+$"])


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

    @staticmethod
    def init_app(app):
        super(DevelopmentConfig, DevelopmentConfig).init_app(app)


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}
