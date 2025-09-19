
import redis
from dotenv import load_dotenv
import os
load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")
r=redis.Redis.from_url(REDIS_URL, decode_responses=True)

DEFAULT_TTL = 60 * 60 * 24 * 7  

def set_url(code: str, original_url: str, ttl: int = DEFAULT_TTL):
    try:
        r.set(code, original_url, ex=ttl)
    except redis.exceptions.ConnectionError:
        print("Warning: Redis not available. Skipping caching.")

def get_url(code: str, ttl: int = DEFAULT_TTL):
    url = r.get(code)
    if url:
        r.expire(code, ttl)  
    return url

