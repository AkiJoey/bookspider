# -*- coding: utf-8 -*-

from redis import StrictRedis

class RedisUtil():
    def __init__(self):
        self.redis = StrictRedis(
            host = 'localhost',
            password = None,
            port = 6379,
            db = 0
        )
	
    def exist(self, key):
        return self.redis.exists(key)

    def save(self, key):
        return self.redis.set(key, '')
