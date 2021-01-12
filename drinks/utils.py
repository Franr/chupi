import redis

from chupi.settings import REDIS_URL


class RedisClient:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
