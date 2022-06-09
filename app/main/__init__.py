from flask import Blueprint, request, jsonify

from .. import app_config
from ..utils.jwtBM import check_token

main = Blueprint('main', __name__)


# -------------------

# 请求之前做权限校验
@main.before_request
def main_before_request():
    url = request.path
    # 请求判断登录状态
    if url not in app_config['WHITE_URL']:
        token = request.headers.get('Authorization')
        res = check_token(token, app_config['EXCHANGE_BM_KEY'])
        if res['errno'] != 0:
            return jsonify(errno=400, error=res)
        else:
            ip = request.headers.get("X-Real-IP", '127.0.0.1')
            if ip != res['data']['ip']:
                return jsonify(errno=400, error="参数校验失败：IP")


# 请每一次请求之后都会调用，会接受一个参数，参数是服务器出现的错误信息
@main.teardown_request
def teardown_request(e):
    print(e, ' ...is error')
    print("teardown_request")
# ----------------------------------------


from . import views, error
