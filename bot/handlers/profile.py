from aiogram import Router, types
from aiogram import F
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.inline import profile_keyboard
from bot.services.users import get_user_balances

router = Router(name="profile")


@router.callback_query(F.data == "profile")
async def profile_handler(callback: types.CallbackQuery, session: AsyncSession) -> None:
    """Profile info"""
    # TODO: Get correct balance (Sum of all wallets)
    balances = await get_user_balances(session, callback.from_user.id)

    text = f"👤<b>Информация о профиле</b>\n\n<b>ID:</b> {callback.from_user.id}\n<b>Общий баланс:</b> {balances['summary_balance']} USDT\n\n<b>Баланс торгового счета</b>: {balances['trading_balance']} USDT\n<b>Баланс депозитных счетов</b>: {balances['deposit_balance']} USDT\n<b>Баланс счетов для вывода</b>: {balances['withdraw_balance']} USDT"

    await callback.message.edit_text(text, reply_markup=profile_keyboard())
    await callback.answer()
