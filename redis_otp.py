import redis


class saveRedisotp:
    redis_host = 'localhost'
    redis_port = 6379
    redis_pass = ''
    redis_db = 0
    rd = redis.Redis(host=redis_host, port=redis_port, password=redis_pass, db=redis_db)

    def __init__(self):
        pass

    @classmethod
    def set_redis(cls, key, value):
        cls.rd.set(key, value)


    def my_delete(cls, key):
        cls.rd.delete(key)

    @classmethod
    def get_redis(cls, key):
        return cls.rd.get(key)



if __name__ == '__main__':
    redis = saveRedisotp()
    redis.set_redis("famliy", "tajik")
    redis.my_delete("num")
