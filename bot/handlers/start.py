from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router(name="start")


@router.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    """Welcome message"""
    await message.answer("Hello!")
