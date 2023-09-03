'''
In this implementation, the `MongoDBSingleton` class ensures that only one instance of the class is created. The `__new__` method is overridden to check if an instance already exists. If an instance doesn't exist, it creates one using the `super().__new__` method.

To use this singleton class, you can create an instance of `MongoDBSingleton` and call its `get_mongo_db()` method to retrieve the MongoDB client.
'''

from pymongo import MongoClient
import threading
import socket


class MongoDBSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, host, port, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, host, port):
        self.client = MongoClient(host, port)

    def get_mongo_db(self):
        return self.client


# MONGO_DB CONFIGURATION DETAILS

HOSTNAME = socket.gethostname()
IPADDRESS = socket.gethostbyname('mongo_db')
MONGO_DB_HOST = IPADDRESS
MONGO_DB_PORT = 27017

myclient = f"mongodb://{MONGO_DB_HOST}:{MONGO_DB_PORT}/"
singleton_mongodb = MongoDBSingleton(myclient, 27017)
