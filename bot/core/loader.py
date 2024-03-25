"""Loader file"""
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from .config import settings

token = settings.BOT_TOKEN

bot = Bot(token=token, parse_mode=ParseMode.HTML)
dp = Dispatcher()
