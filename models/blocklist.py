from redisca import Model, String
from redisca import conf
from redis import Redis


@conf(db=Redis('redis', port=6379))
class BlockList(Model):
    jti = String(
        field='jti',
        unique=True
    )


def is_in_list(jti):
    data = BlockList.jti.find(jti)
    if data:
        return True
    else:
        return False
