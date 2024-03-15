from aiogram import Router, types
from aiogram import F
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.inline import profile_keyboard, history_keyboard
from bot.services.users import get_user_balance

router = Router(name="profile")


@router.callback_query(F.data == "profile")
async def profile_handler(callback: types.CallbackQuery, session: AsyncSession) -> None:
    """Profile info"""
    balance = await get_user_balance(session, callback.from_user.id)

    text = f"👤<b>Информация о профиле</b>\n\n<b>ID:</b> {callback.from_user.id}\n<b>Баланс:</b> {balance} USDT"

    await callback.message.edit_text(text, reply_markup=profile_keyboard())
    await callback.answer()


@router.callback_query(F.data == "history")
async def history_handler(callback: types.CallbackQuery) -> None:
    """History info"""
    await callback.message.edit_text("📝<b>История транзакций</b>\n\nВы пока не совершили ни одной транзакции",
                                     reply_markup=history_keyboard())
    await callback.answer()
