"""
Redis 및 Celery 설정
"""

from decouple import config

REDIS_URL = config("REDIS_URL", cast=str)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    },
}

CELERY_BROKER_URL = REDIS_URL

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
