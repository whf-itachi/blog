from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy

from config import config

mail = Mail()
moment = Moment()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    print(app.name, '...')
    app.config.from_object(config['development'])

    # 实例化SQLAlchemy对象
    db = SQLAlchemy(app)
    # 第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例
    migrate = Migrate(app, db)

    # mail.init_app(app)
    # moment.init_app(app)
    # db.init_app(app)
    # login_manager.init_app(app)
    # pagedown.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app, db
