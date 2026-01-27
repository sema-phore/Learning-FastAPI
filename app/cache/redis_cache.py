import os
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

redis_client = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)


def get_cached_prediction(key: str):
    value = redis_client.get(key)
    return eval(value) if value else None


def set_cached_prediction(key: str, value: dict):
    redis_client.set(key, str(value))







"""
import json 
import redis
from app.core.config import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL)

# Get from cache
def get_cached_prediction(key: str):
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None

def set_cached_prediction(key: str, value: dict, expiry: int = 3600):
    redis_client.setex(key, expiry, json.dumps(value))



If Redis fails/breaks, continue normlly without cache

def get_cached_prediction(key: str):
    try:
        value = redis_client.get(key)
        return json.loads(value) if value else None
    except redis.RedisError:
        return None

except redis.RedisError: 
This catches any Redis-related error, for example:
- ConnectionError
- TimeoutError
- AuthenticationError

then continue with out cache

"""