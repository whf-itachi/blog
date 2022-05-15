import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = ''

    pass


class DevelopConfig(Config):
    DEBUG = True


class ProductConfig(Config):
    DEBUG = False


config = {
    'development': DevelopConfig,
    'production': ProductConfig,

    'default': DevelopConfig
}
