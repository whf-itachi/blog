from flask import Blueprint


main = Blueprint('main', __name__)


# -------------------
# 请每一次请求之后都会调用，会接受一个参数，参数是服务器出现的错误信息
@main.teardown_request
def teardown_request(e):
    print(e, ' ...is error')
    print("teardown_request")
# ----------------------------------------


from . import views, error
