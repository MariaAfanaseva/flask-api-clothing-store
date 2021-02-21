import os
from datetime import timedelta
from redis import StrictRedis


redis_db = StrictRedis('redis', port=6379, db=0)


def add_jti_token(jti):
    access_time = timedelta(hours=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES')))
    redis_db.set(name=jti, value='', ex=access_time)


def is_jti_blocklisted(jti):
    return redis_db.exists(jti)


def print_data():
    for key in redis_db.scan_iter():
        value = redis_db.get(key)
        print(f'{key}: {value}')


def clear_db():
    redis_db.flushdb()
