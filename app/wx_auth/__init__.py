# -*- coding: utf-8 -*-
# filename: handle.py
import datetime
import hashlib
from flask import request, Blueprint
import requests

from app import app_config
import logging

log = logging.getLogger(__name__)

wx = Blueprint('wx', __name__)


@wx.route('/', methods=('GET', 'POST'))
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
        log.info("wx_token_check, hashcode:%s, signature:%s", hashcode, signature)
        if hashcode == signature:
            return echostr
    return ""


# 获取用户的微信唯一openid
def get_user_info_by_openid(openid, access_token):
    url = 'https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}&lang=zh_CN'.format(
        access_token=access_token, openid=openid)
    response = requests.get(url)
    response.encoding = 'utf-8'
    json_data = response.json() if response and response.json() else None
    '''
    {"openid":"oLjaZ0QlzPIIOKhcoediTvNrRfw0",
    "nickname":"itachi",
    "sex":1,
    "language":"zh_CN",
    "city":"",
    "province":"施蒂利亚",
    "country":"奥地利",
    "headimgurl":"http:\/\/thirdwx.qlogo.cn\/mmopen\/vi_3\/
    DYAIOgq83erb9KD8YAjeD3W5KbsKMv7OveobNk8a20uqNZuwEYNtYrxric6fgxJDbMolS5LV4GHslhD6b0U72gQ\/132",
    "privilege":[]}
    '''

    return json_data


