import redis as redis
from flask import g

config = {
    'host': '127.0.0.1',
    'port': 6379,
    'password': '',
    'db': 0,
    'decode_responses': True
}


# 连接redis
def connect_redis():
    return redis.Redis(**config)


# 获取redis连接对象
def get_redis():
    if not g:
        return connect_redis()

    if not hasattr(g, 'redis'):
        g.redis = connect_redis()
    return g.redis
