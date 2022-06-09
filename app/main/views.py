from datetime import datetime
from flask import redirect, render_template, session, url_for, jsonify, request
from werkzeug.exceptions import abort
from werkzeug.wrappers import response

from . import main
from .. import db
from ..models import Post, User


# 上传博客
@main.route('/blog/upload', methods=["POST"])
def upload_blog():
    req_data = request.form.to_dict()
    print(req_data)
    blog_data = req_data.get("blog")
    user_id = req_data.get("user_id")
    bolg_id = req_data.get("bolg_id")

    if bolg_id:
        # 更新博客内容
        print('modify a blog')
        blog_db = Post.query.filter_by(id=bolg_id).first()
        blog_db.body = blog_data
    else:
        # 新增用户博客
        print('create a blog')
        blog_db = Post(user_id, blog_data)
    db.session.add(blog_db)
    db.session.commit()

    return jsonify(errno=0, error='success')


# 获取博客信息
@main.route('/blog/query', methods=['GET'])
def get_blog_info():

    post_info = Post.query.all()

    post_infos = []

    for post in post_info:
        post_infos.append(post.to_dict())

    return jsonify(errno=0, error='success', data=post_infos)

# -------------------------- 以下为测试代码 ---------------------------------


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
