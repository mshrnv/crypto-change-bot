"""Main module"""
from __future__ import annotations
import asyncio
import logging

from core.loader import bot, dp
from database.database import async_main, engine

from handlers import get_handlers_router
from middlewares import register_middlewares


async def on_startup() -> None:
    """On bot start actions"""
    logging.info('Bot starting...')

    register_middlewares(dp)
    dp.include_router(get_handlers_router())

    bot_info = await bot.get_me()

    logging.info(f"Name     - {bot_info.full_name}")
    logging.info(f"Username - @{bot_info.username}")
    logging.info(f"ID       - {bot_info.id}")

    logging.info("Bot started 🚀")


async def on_shutdown() -> None:
    """On bot shutdown actions"""
    logging.info("Bot stopping...")

    await dp.storage.close()
    await dp.fsm.storage.close()

    await bot.session.close()

    logging.info("Bot stopped 🖥️")


async def main() -> None:
    """Start bot"""
    logging.basicConfig(level=logging.INFO)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await async_main(_engine=engine)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
