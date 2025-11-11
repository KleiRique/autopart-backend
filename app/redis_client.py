import redis
from app.settings import settings
redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
def cache_setex(key: str, value: str, ttl: int): redis_client.setex(key, ttl, value)
