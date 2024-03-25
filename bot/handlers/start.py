"""Base handler"""
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession

from bot.data.messages import START_MESSAGE, MENU_MESSAGE
from bot.keyboards.inline import main_keyboard
from bot.services.users import user_exists, add_user

router = Router(name="start")


@router.message(CommandStart())
async def start_handler(message: types.Message, session: AsyncSession) -> None:
    """Welcome message"""

    if not await user_exists(session, message.from_user.id):
        await add_user(session, message.from_user)

    await message.answer(START_MESSAGE)
    await message.answer(MENU_MESSAGE, reply_markup=main_keyboard())


@router.message(Command("menu"))
async def menu_handler(message: types.Message):
    """Menu message"""
    await message.answer(MENU_MESSAGE, reply_markup=main_keyboard())


@router.callback_query(F.data == "menu")
async def edit_menu_handler(callback: types.CallbackQuery):
    """Menu message"""
    await callback.message.edit_text(MENU_MESSAGE, reply_markup=main_keyboard())
    await callback.answer()


@router.callback_query(F.data == "new_menu")
async def new_menu_handler(callback: types.CallbackQuery):
    """Menu message"""
    await callback.message.answer(MENU_MESSAGE, reply_markup=main_keyboard())
