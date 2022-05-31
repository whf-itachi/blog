import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@127.0.0.1:3306/test'  # mysql://username:password@hostname/database
    # # 动态追踪修改设置，如未设置只会提示警告
    # SQLALCHEMY_TRACK_MODIFICATIONS = True
    # # 查询时会显示原始SQL语句
    # SQLALCHEMY_ECHO = True
    # # 每次请求结束后都会自动提交数据库中的变动
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SECRET_KEY = 'hard to guess string'


class DevelopConfig(Config):
    DEBUG = True


class ProductConfig(Config):
    DEBUG = False


config = {
    'development': DevelopConfig,
    'production': ProductConfig,

    'default': DevelopConfig
}
