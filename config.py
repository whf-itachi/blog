import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/test'
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True

    SECRET_KEY = ''


class DevelopConfig(Config):
    DEBUG = True


class ProductConfig(Config):
    DEBUG = False


config = {
    'development': DevelopConfig,
    'production': ProductConfig,

    'default': DevelopConfig
}
