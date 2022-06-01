from datetime import datetime
from flask import redirect, render_template, session, url_for, jsonify, request
from werkzeug.exceptions import abort

from . import main
from ..models import Post, User


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


@main.route("/", methods=['GET', 'POST'])
def index():

    # 按创建时间进行降序排列
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    print(posts, ' posts')

    return jsonify(data={"posts": "posts", "form": "form"})
    # return render_template('index.html', form=form, posts=posts)


@main.route("/create", methods=['POST'])
def create():
    # if current_user.can(Permission.WRITE) and form.submit():
    #     author = current_user._get_current_object()
    #     post = Post(body=form.body.data, author=author)
    #     db.session.add(post)
    #     return redirect(url_for('.index'))

    # 按创建时间进行降序排列
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    print(posts, ' posts')

    return jsonify(data={"posts": "posts", "form": "form"})
    # return render_template('index.html', form=form, posts=posts)


@main.route('/user/<username>')
def user(username):
    user_data = User.query.filter_by(username=username).first()
    if user_data is None:
        abort(404)

    posts = user_data.posts.order_by(Post.timestamp.desc()).all()

    return render_template('user.html', user=user_data, posts=posts)
