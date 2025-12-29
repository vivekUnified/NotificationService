import time
import redis
from django.conf import settings

# Initialize Redis client for rate limiting
# We use the same Redis as Celery for simplicity, but ideally should be separate db
redis_client = redis.Redis.from_url(settings.CELERY_RESULT_BACKEND)

class RateLimiter:
    def __init__(self, limit=5, window=60):
        """
        :param limit: Number of allowed requests
        :param window: Time window in seconds
        """
        self.limit = limit
        self.window = window

    def is_allowed(self, user_id, channel):
        """
        Check if the user is allowed to receive a notification on this channel.
        """
        try:
            key = f"rate_limit:{user_id}:{channel}"
            current_time = int(time.time())
            window_start = current_time - self.window

            # Remove old entries
            redis_client.zremrangebyscore(key, 0, window_start)

            # Count current entries
            count = redis_client.zcard(key)

            if count < self.limit:
                # Add new entry
                redis_client.zadd(key, {str(current_time): current_time})
                # Set expiry for the key to avoid clutter
                redis_client.expire(key, self.window + 10)
                return True
            
            return False
        except redis.exceptions.ConnectionError:
            # Fallback: Allow if Redis is down (Fail Open)
            return True
        except Exception as e:
            # Log other errors but allow
            print(f"Rate Limiter Error: {e}")
            return True
