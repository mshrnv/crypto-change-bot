"""Init middlewares module"""
from aiogram import Dispatcher

from bot.middlewares.database import DatabaseMiddleware


def register_middlewares(dp: Dispatcher) -> None:
    """Registering all bot middlewares"""
    dp.update.outer_middleware(DatabaseMiddleware())
