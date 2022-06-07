# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
from flask import request

from app import app_config
from app.main import main
# import logging
#
# log = logging.getLogger(__name__)


@main.route('/handle', methods=('GET', 'POST'))
def wx_token_check():
    print('get here! wx_token_check')
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    token = app_config['WX_TOKEN']

    if signature and timestamp and nonce and echostr:
        dataList = [timestamp, token, nonce]
        dataList.sort()
        sha1Obj = hashlib.sha1()
        for item in dataList:
            sha1Obj.update(item.encode('UTF-8'))
        hashcode = sha1Obj.hexdigest()
        # log.info("wx_token_check, hashcode:%s, signature:%s", hashcode, signature)
        if hashcode == signature:
            return echostr
    return ""
