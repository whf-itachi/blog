from datetime import datetime

from . import db


class User(db.Model):
    __tablename__ = 'users'  # 类变量 定义在数据库中使用的表名
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), unique=True, index=True)
    user_phone = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(255))
    create_time = db.Column(db.Time, default=datetime.now)
    update_time = db.Column(db.Time, default=datetime.now, onupdate=datetime.now)
    last_login_time = db.Column(db.Time)
    last_login_ip = db.Column(db.String(64))
    login_count = db.Column(db.Integer)
    # posts = db.relationship('Post', backref='author', lazy='dynamic')
    # role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, user_name, user_phone, email, password_hash):
        self.user_name = user_name
        self.user_phone = user_phone
        self.email = email
        self.password_hash = password_hash

    # 返回一个具有可读性的字符串表示模型，可在调试和测试时使用。
    def __repr__(self):
        return '<User %s>' % self.user_name


# class Role(db.Model):
#     # 定义表名
#     __tablename__ = 'roles'
#     # 定义列对象
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     us = db.relationship('User', backref='role')
#
#     # repr()方法显示一个可读字符串
#     def __repr__(self):
#         return 'Role:%s'% self.name

# 定义模型类-作者
class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    au_book = db.relationship('Book', backref='author')  # backref 在关系的另一个模型中添加反向引用: Book中有个author属性

    def __repr__(self):
        return 'Author:%s' % self.name


# 定义模型类-书名
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    au_book = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __str__(self):
        return 'Book:%s,%s' % (self.info, self.lead)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        dict_data = {
            "id": self.id,
            "body": self.body,
            "timestamp": self.timestamp,
            "author_id": self.author_id
        }

        return dict_data
