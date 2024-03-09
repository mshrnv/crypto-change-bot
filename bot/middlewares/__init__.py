from aiogram import Dispatcher

from bot.middlewares.auth import AuthMiddleware
from bot.middlewares.database import DatabaseMiddleware


def register_middlewares(dp: Dispatcher) -> None:
    dp.update.outer_middleware(DatabaseMiddleware())
    dp.message.middleware(AuthMiddleware())
