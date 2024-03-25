"""Settings handlers"""
from random import choice

from aiogram import Router, types
from aiogram import F
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.config import settings
from bot.data.messages import HELP_MESSAGE
from bot.keyboards.inline import support_keyboard, settings_keyboard, write_to_support_keyboard
from bot.services.users import get_notifications_status, change_notifications_status

router = Router(name="settings")


@router.callback_query(F.data == "support")
async def support_handler(callback: types.CallbackQuery) -> None:
    """Support info"""
    await callback.message.edit_text(HELP_MESSAGE, reply_markup=support_keyboard())
    await callback.answer()


@router.callback_query(F.data == "write_to_support")
async def write_to_support_handler(callback: types.CallbackQuery) -> None:
    """Write to support"""
    await callback.message.edit_text(
        f"🔋Для получения помощи, свяжитесь с администратором: @{settings.SUPPORT_USERNAME}",
        reply_markup=write_to_support_keyboard())
    await callback.answer()


@router.callback_query(F.data == "settings")
async def settings_handler(callback: types.CallbackQuery, session: AsyncSession) -> None:
    """Settings"""

    notifications_status = await get_notifications_status(session, callback.from_user.id)

    await callback.message.edit_text("<b>Настройка работы бота</b> ⚙️",
                                     reply_markup=settings_keyboard(notifications_status))
    await callback.answer()


@router.callback_query(F.data == "change_notifications_status")
async def change_notifications_status_handler(callback: types.CallbackQuery, session: AsyncSession) -> None:
    """Change notification status"""

    notifications_status = await change_notifications_status(session, callback.from_user.id)

    # TODO: СТРАШНЫЙ КОСТЫЛЬ
    smiles = ['🔧', '🔨', '🛠', '🪛', '⚙️', '🔩', '🪜', '🖇', '📐', '🗃', '🗳']
    await callback.message.edit_text(f"<b>Настройка работы бота</b> {choice(smiles)}",
                                     reply_markup=settings_keyboard(notifications_status))
    await callback.answer()
