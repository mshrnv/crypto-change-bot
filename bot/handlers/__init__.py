from aiogram import Router
from . import start, profile, settings, transactions


def get_handlers_router() -> Router:
    router = Router()

    router.include_router(start.router)
    router.include_router(profile.router)
    router.include_router(settings.router)
    router.include_router(transactions.router)

    return router
