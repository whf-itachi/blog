from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'  # 类变量 __tablename__ 定义在数据库中使用的表名
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(64))
    # role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 返回一个具有可读性的字符串表示模型，可在调试和测试时使用。
    def __repr__(self):
        return '<User %f>' % self.username


@login_manager.user_loader
def load_user(user_id):
    """
    加载用户的回调函数接收以 Unicode 字符串形式表示的用户标识符。如果能找到用户，这
个函数必须返回用户对象；否则应该返回 None。
    :param user_id:
    :return:
    """
    return User.query.get(int(user_id))


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
