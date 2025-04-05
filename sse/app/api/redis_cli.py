# import redis
#
#
# class RedisClient:
#     client = None
#
#     def __new__(cls, *args, **kwargs):
#         if not cls.client:
#             cls._instance =
#         return cls.client

# api/redis_cli.py
import redis


class RedisClient:
    _instance = None

    def __new__(cls):
        """Create a single instance of RedisClient"""
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            # Initialize the Redis connection only once
            cls._instance.client = redis.StrictRedis(
                    host="redis-18557.c99.us-east-1-4.ec2.redns.redis-cloud.com",
                    port=18557,
                    password="pr5cFAGESzhvgoHZAlPVEFuan3VBsf0u",
                    decode_responses=True
            )
        return cls._instance

    @classmethod
    def get_instance(cls):
        """Alternative method to get the singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def publish(self, channel, message):
        return self.client.publish(channel, message)

    def pubsub(self):
        return self.client.pubsub()

    def sadd(self, key, value):
        return self.client.sadd(key, value)

    def srem(self, key, value):
        return self.client.srem(key, value)

    def smembers(self, key):
        return self.client.smembers(key)

    def setex(self, key, ttl, value):
        return self.client.setex(key, ttl, value)

    def get(self, key):
        return self.client.get(key)

    def set(self, key, value):
        return self.client.set(key, value)

    def keys(self, pattern):
        return self.client.keys(pattern)

    def delete(self, key):
        return self.client.delete(key)

    def ping(self):
        """Check if Redis connection is alive"""
        return self.client.ping()
