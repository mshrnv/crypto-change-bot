from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from redis.asyncio import ConnectionPool, Redis

from .config import settings

redis_client = Redis(
    connection_pool=ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASS,
        db=0,
    ),
)

storage = RedisStorage(
    redis=redis_client,
    key_builder=DefaultKeyBuilder(with_bot_id=True),
)

token = settings.BOT_TOKEN

bot = Bot(token=token, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=storage)

DEBUG = settings.DEBUG
