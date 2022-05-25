from flask import render_template
from flask_login import login_required

from . import auth


@auth.route('/login')
def login():
    print('login is run')
    return render_template('auth/login.html')


@auth.route('/secret')
@login_required
def secret():
    """
    login_required 修饰器:
        如果未认证的用户访问这个路由，Flask-Login 会拦截请求，把用户发往登录页面。
    :return:
    """
    return 'Only authenticated users are allowed!'

