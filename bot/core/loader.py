from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from .config import settings

token = settings.BOT_TOKEN
DEBUG = settings.DEBUG

bot = Bot(token=token, parse_mode=ParseMode.HTML)
dp = Dispatcher()
