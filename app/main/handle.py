# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
from flask import request

from app import app_config
from app.main import main
import logging

log = logging.getLogger(__name__)


class Handle(object):
    def GET(self):
        try:
            data = request.get_json()
            print(data, 'dddddddddddddd')
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "N12W4ECVjXt8cmLs"  # 请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as e:
            return e


@main.route('/', methods=('GET', 'POST'))
def wx_token_check():
    print('get here! wx_token_check')
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    token = app_config.config['WX_TOKEN']

    if signature and timestamp and nonce and echostr:
        dataList = [timestamp, token, nonce]
        dataList.sort()
        sha1Obj = hashlib.sha1()
        for item in dataList:
            sha1Obj.update(item.encode('UTF-8'))
        hashcode = sha1Obj.hexdigest()
        log.info("wx_token_check, hashcode:%s, signature:%s", hashcode, signature)
        if hashcode == signature:
            return echostr
    return ""
