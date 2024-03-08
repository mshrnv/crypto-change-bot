from aiogram import Dispatcher


def register_middlewares(dp: Dispatcher) -> None:
    from .database import DatabaseMiddleware

    dp.update.outer_middleware(DatabaseMiddleware())
