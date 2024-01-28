import redis


class Store:

    def __init__(self, host='localhost', port=6379, db=0) -> None:
        self.r = redis.Redis(host=host, port=port, db=db)

    def get(self, key):
        return self.r.get(key)

    def cache_get(self, key):
        try:
            return self.get(key)
        except redis.RedisError:
            return None

    def cache_set(self, key, value, ttl):
        try:
            self.r.set(key, value, ex=ttl)
        except redis.RedisError:
            pass
        