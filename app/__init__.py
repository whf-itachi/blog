import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import pymysql

from config import config

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


# 其他配置信息
app_config = dict(
    JWT_EXPIRED_SECONDS=86400,  # token过期时间
    EXCHANGE_BM_KEY='H9KDmQsnEviC1hofWlTX35711L1pKhjkB4fKAVFrWUdtB6h68ZhJJoDCTacqTYv',
    PW_ENCRYPT_ALG='pbkdf2:sha256:50000',
    WX_TOKEN='N12W4ECVjXt8cmLs',
)


pymysql.install_as_MySQLdb()
# 实例化SQLAlchemy对象
db = SQLAlchemy()  # db 对象是 SQLAlchemy 类的实例，表示程序使用的数据库，同时还获得了 Flask-SQLAlchemy 提供的所有功能。
migrate = Migrate()

login_manager = LoginManager()
# 安全等级， None、basic、strong
login_manager.session_protection = 'strong'  # strong会记录客户端ip和代理信息，如果发现移动就登出用户
login_manager.login_view = 'auth.login'  # 设置登录页面的端点


def create_app():
    app = Flask(__name__)
    app.config.from_object(config['development'])

    db.init_app(app)
    migrate.init_app(app, db)  # 第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例

    login_manager.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
