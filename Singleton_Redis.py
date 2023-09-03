'''
In this implementation, the `RedisSingleton` class ensures that only one instance of the class is created. The `__new__` method is overridden to check if an instance already exists. If an instance doesn't exist, it creates one using the `super().__new__` method.

To use this singleton class, you can create an instance of `RedisSingleton` and call its `get_redis_client()` method to retrieve the Redis Client.
'''

import redis
import threading
import socket


class RedisSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, host, port,  *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, host, port):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)

    def get_redis_client(self):
        return self.client

# REDIS CONFIGURATION DETAILS


HOSTNAME = socket.gethostname()
IPADDRESS = socket.gethostbyname('redis_db')
REDIS_DB_HOST = IPADDRESS
REDIS_DB_PORT = 6379

redis_client = RedisSingleton(REDIS_DB_HOST, REDIS_DB_PORT)
