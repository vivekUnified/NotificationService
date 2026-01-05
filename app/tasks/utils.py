import time
import redis
from app.core.config import settings

# Initialize Redis client 
redis_client = redis.Redis.from_url(settings.CELERY_RESULT_BACKEND)

class RateLimiter:
    def __init__(self, limit=5, window=60):
        self.limit = limit
        self.window = window

    def is_allowed(self, user_id, channel):
        try:
            key = f"rate_limit:{user_id}:{channel}"
            current_time = int(time.time())
            window_start = current_time - self.window

            pipeline = redis_client.pipeline()
            pipeline.zremrangebyscore(key, 0, window_start)
            pipeline.zcard(key)
            pipeline.zadd(key, {str(current_time): current_time})
            pipeline.expire(key, self.window + 10)
            results = pipeline.execute()
            
            count = results[1]
            if count < self.limit:
                return True
            return False
        except Exception as e:
            print(f"Rate Limiter Error: {e}")
            return True
