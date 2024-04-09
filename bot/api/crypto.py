from redis import Redis

from bot.core.config import settings

redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=1,
    charset="utf-8",
    decode_responses=True
)


def get_spreads():
    """Returns all spreads from Redis DB"""
    data = {}
    keys = redis_client.keys('*')
    for key in keys:
        data[key] = redis_client.hgetall(key)

    return data
