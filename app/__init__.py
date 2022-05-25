from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import config

# mail = Mail()
# moment = Moment()
# pagedown = PageDown()

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
    print(app.name, '...')

    db.init_app(app)
    migrate.init_app(app, db)  # 第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例

    login_manager.init_app(app)

    # mail.init_app(app)
    # moment.init_app(app)
    # pagedown.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
