from aiogram import Router, types
from aiogram import F
# from sqlalchemy.ext.asyncio import AsyncSession

from bot.data.messages import HELP_MESSAGE
from bot.keyboards.inline import support_keyboard, settings_keyboard

router = Router(name="settings")


@router.callback_query(F.data == "support")
async def profile_handler(callback: types.CallbackQuery) -> None:
    """Support info"""
    await callback.message.edit_text(HELP_MESSAGE, reply_markup=support_keyboard())
    await callback.answer()


@router.callback_query(F.data == "settings")
async def profile_handler(callback: types.CallbackQuery) -> None:
    """Support info"""
    await callback.message.edit_text("Здесь будут настройки бота", reply_markup=settings_keyboard())
    await callback.answer()
