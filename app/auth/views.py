import json
import re

from flask import jsonify, session, request, g
from werkzeug.security import generate_password_hash, check_password_hash

from app import app_config, db
from app.auth import auth

from app.models import User
from app.utils.imgCodeUtil import img_base64_encode
from app.utils.jwtBM import create_token
from app.utils.redis_db import get_redis


#  登录
@auth.route('/login', methods=['POST'])
def bp_login():
    # 获取表单提交数据
    data = request.form.to_dict()
    password = data['password']
    account_name = data['account_name']
    if not isinstance(account_name, str) or len(account_name) > 50:
        return jsonify(errno=400, error='error')

    # 允许用户以手机作为用户名登录
    if re.match(r'^1[3456789]\d{9}$', account_name):
        user_name = None
        user_phone = account_name
    else:
        user_name = account_name
        user_phone = None

    try:
        #   校验验证码
        rdb = get_redis()
        ip = request.headers.get("X-Real-IP", '127.0.0.1')
        key = ip + '_img_code'
        redis_user_info = rdb.get(key)
        redis_info_dict = json.loads(redis_user_info) if redis_user_info else None
        if redis_user_info and redis_info_dict.get('img_code'):
            img_code = request.form.get('img_code') if not request.get_json() else request.get_json().get(
                'img_code')
            if not img_code or img_code != redis_info_dict.get('img_code'):
                return jsonify(errno=400, error='img_code is wrong')

        if user_name is not None:
            # 根据用户名查询用户
            user_info = User.query.filter_by(user_name=user_name).first()
        else:
            # 根据手机号查询用户
            user_info = User.query.filter_by(user_phone=user_phone).first()

        if not user_info or not user_info['password_hash']:
            if redis_user_info:
                count = redis_info_dict['count'] + 1
                value = {
                    'img_code': None,
                    'count': count,
                    'img_code_str': ''
                }

                if count > 2:
                    img_code_str, code = img_base64_encode()
                    value = {
                        'img_code': code,
                        'count': count,
                        'img_code_str': img_code_str
                    }
                rdb.set(key, json.dumps(value), 600)
            else:
                value = {
                    'img_code': None,
                    'count': 0,
                    'img_code_str': ''
                }
                rdb.set(key, json.dumps(value), 600)
            return jsonify(errno=400, error='account_name or password is wrong')

        #   校验密码
        user_pwd = user_info['user_pwd']
        if not check_password_hash(user_pwd, password):

            if redis_user_info:
                count = redis_info_dict['count'] + 1
                value = {
                    'img_code': None,
                    'count': count,
                    'img_code_str': ''
                }

                if count > 2:
                    img_code_str, code = img_base64_encode()
                    value = {
                        'img_code': code,
                        'count': count,
                        'img_code_str': img_code_str
                    }
                rdb.set(key, json.dumps(value), 600)
            else:
                value = {
                    'img_code': None,
                    'count': 0,
                    'img_code_str': ''
                }
                rdb.set(key, json.dumps(value), 600)

            return jsonify(errno=400, error='account_name or password is wrong')

        # 更新登陆地点与登录次数，后续再做登陆地域进行判断告警
        # last_login_ip = user_info['last_login_ip']
        last_login_time = user_info['last_login_time']
        user_info.last_login_ip = request.headers.get("X-Real-IP", '127.0.0.1')
        user_info.last_login_time = last_login_time
        user_info.login_count = user_info.login_count + 1

        # 确认登陆，返回token
        ip = request.headers.get("X-Real-IP", '127.0.0.1')
        # print('登陆ip：'+ip)
        token = create_token({'user': user_info['user_name'], 'ip': ip}, app_config['EXCHANGE_BM_KEY'])
        #   删除验证码图片
        rdb.delete(key)

        return jsonify(errno=0, token=token, user_name=user_info['user_name'])

    except Exception as e:
        return jsonify(errno=500, error='System error')


#  登出
@auth.route('/logout', methods=['POST'])
def bp_logout():
    # 清除会话记录
    session.clear()
    return jsonify(errno=0, error=0)


#  注册
@auth.route('/register', methods=['POST'])
def bp_register():
    try:
        data = request.form.to_dict()

        user_name = data['user_name']
        user_phone = data['user_phone']
        password = data['password']
        email = data['email']

        # 判断手机号,用户名是否已经注册
        select_flag = User.query.filter_by(user_phone=user_phone).first()
        if select_flag:
            return jsonify(errno=400, error='The phone already exists')
        select_flag = User.query.filter_by(user_name=user_name).first()
        if select_flag:
            return jsonify(errno=400, error='The user_name already exists')

        password_hash = generate_password_hash(password, app_config['PW_ENCRYPT_ALG'])

        # 新增用户信息
        new_user = User(user_name, user_phone, email, password_hash)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(errno=0, error='success')

    except Exception as e:
        return jsonify(errno=500, error=f'System error:{e}')
