import redis


class RedisDriver():
    """
    Class that interact with Redis K/V
    """
    def __init__(self):
        db_host = 'localhost'
        db_port = '6379'
        db_num = 1
        db_pwd = None
        self.redis = redis.StrictRedis(host=db_host, port=db_port, db=db_num, password=db_pwd)

    def set_value(self, type, field, value):
        self.redis.hset(type, field, value)

    def get_value(self, type, field):
        return self.redis.hget(type, field)

    def get_all(self, type):
        return self.redis.hgetall(type)
