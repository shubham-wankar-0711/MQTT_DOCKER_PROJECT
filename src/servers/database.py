from Singleton_MongoDB import singleton_mongodb
from Singleton_Redis import redis_client

# GETTING SINGLETON MONGO_DB CLIENT
mongodb_client = singleton_mongodb.get_mongo_db()

# GETTING SINGLETON REDIS CLIENT
redis_client = redis_client.get_redis_client()
