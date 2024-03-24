from aiogram import Router
from . import start, profile, settings, wallets


def get_handlers_router() -> Router:
    router = Router()

    router.include_router(start.router)
    router.include_router(profile.router)
    router.include_router(settings.router)
    router.include_router(wallets.router)

    return router
