import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'QWEQWJKELAKJDLKJSD'
    # FIXME
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'LGJLKASJDJLKJLKJQWE'
    REFRESH_EXP_LENGTH = 300
    ACCESS_EXP_LENGTH = 100
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
