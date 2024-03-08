from aiogram import Router, types
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.users import add_user, user_exists

router = Router(name="start")


@router.message(CommandStart())
async def start_handler(message: types.Message, session: AsyncSession) -> None:
    """Welcome message"""
    if not await user_exists(session, message.from_user.id):
        await add_user(session, message.from_user, None)
    await message.answer("Hello!")
