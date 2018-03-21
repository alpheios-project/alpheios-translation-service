import os
from warnings import warn


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    APP_NAME = 'Pandora PostCorrection Editor'
    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        SECRET_KEY = 'SECRET_KEY_ENV_VAR_NOT_SET'
        warn('SECRET KEY ENV VAR NOT SET! SHOULD NOT SEE IN PRODUCTION')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class TestConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    warn('THIS APP IS IN TEST MODE. YOU SHOULD NOT SEE THIS IN PRODUCTION.')


config = {
    "test": TestConfig
}
