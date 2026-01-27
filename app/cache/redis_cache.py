import os
import json
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

redis_client = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)


def get_cached_prediction(key: str):
    try:
        value = redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    except (redis.RedisError, json.JSONDecodeError):
        return None


def set_cached_prediction(key: str, value: dict, expiry: int = 3600):
    redis_client.setex(key, expiry, json.dumps(value))







"""
If Redis fails/breaks, continue normlly without cache

def get_cached_prediction(key: str):
    try:
        value = redis_client.get(key)
        return json.loads(value) if value else None
    except (redis.RedisError, json.JSONDecodeError):
        return None

except (redis.RedisError, json.JSONDecodeError): 
This catches any Redis-related error, for example:
- ConnectionError
- TimeoutError
- AuthenticationError

then continue with out cache

"""