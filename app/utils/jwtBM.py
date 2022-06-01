import jwt
import time

from app import app_config

headers = {
    'alg': 'HS256',
    'typ': 'JWT'
}


def create_token(data, secret):
    if not data or not isinstance(data, dict):
        return None

    payload = {
        'exp': int(time.time() + app_config['JWT_EXPIRED_SECONDS'])
    }
    payload.update(data)
    token = jwt.encode(payload, secret, algorithm='HS256')

    return token


# def checkToken(token, secret):
#     if not token:
#         return dict(errno=ErrAuthMissToken, error='Missing token')
#     try:
#         # secret = app.config['SECRET_KEY']
#         decode = jwt.decode(token, secret, algorithms='HS256')
#         # print(decode)
#     except jwt.ExpiredSignatureError:
#         return dict(errno=ErrAuthTokenExp, error='Token expired. Please log in again.')
#     except jwt.exceptions.DecodeError:
#         return dict(errno=ErrAuthTokenMissSeg, error='Not enough segments')
#     except jwt.InvalidTokenError:
#         return dict(errno=ErrAuthInvalidToken, error='Invalid token. Please log in again.')
#     except:
#         return dict(errno=ErrAuthInvalidFormat, error='Invalid token format')
#     else:
#         return dict(errno=Err_Suc, error='success', data=decode)


if __name__ == "__main__":
    print(create_token({'user': 'xy_super_admin', 'ip': '127.0.0.1'}, app_config['EXCHANGE_BM_KEY']))
    print(create_token({'user': 'xy_agent', 'ip': '127.0.0.1'}, app_config['EXCHANGE_BM_KEY']))

