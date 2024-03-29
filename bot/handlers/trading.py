"""Trading operations handlers"""
from aiogram import Router, types
from aiogram import F
from aiogram import html
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.data.callback import TransferToTradingWalletCallbackFactory
from bot.data.states import WithdrawOrder, TransferToTradingWallet

from bot.keyboards.inline import wallets_keyboard, new_menu_keyboard, approve_transfer_to_trading_wallet_keyboard, \
    back_to_menu_keyboard
from bot.services.transfers import add_transfer_transaction
from bot.services.wallets import get_wallet_info

router = Router(name="trading")


@router.callback_query(TransferToTradingWalletCallbackFactory.filter())
async def transfer_to_trading_wallet_handler(
        callback: types.CallbackQuery,
        callback_data: TransferToTradingWalletCallbackFactory,
        state: FSMContext,
        session: AsyncSession
) -> None:
    """Wallets categories"""
    await callback.message.edit_text(
        text="🧾Введите сумму перевода на торговый счет в USDT"
    )

    from_wallet = await get_wallet_info(session, callback_data.wallet_id)
    await state.update_data(from_wallet=from_wallet)

    await state.set_state(TransferToTradingWallet.amount)
    await callback.answer()


@router.message(TransferToTradingWallet.amount)
async def amount_transfer_to_trading_handler(message: types.Message, state: FSMContext):
    """Entering amount to transfer to trading wallet"""

    try:
        amount = float(message.text)
        # TODO: Check balance !!!
        await state.update_data(amount=amount)

        user_data = await state.get_data()
        await message.answer(
            text=f"🧾<b>Подтвердите данные перевода на торговый счет</b>:\n\nКошелек-источник (ID-{user_data.get('from_wallet').id}):\n{html.pre(user_data.get('from_wallet').base58_address)}\n\nСумма перевода:\n{user_data.get('amount')} USDT\n\nВы уверены, что хотите совершить перевод?",
            reply_markup=approve_transfer_to_trading_wallet_keyboard()
        )

        await state.set_state(TransferToTradingWallet.approve)
    except ValueError:
        await message.answer(
            text="Неверно введена сумма для перевода, попробуйте еще раз 🔄"
        )


@router.callback_query(F.data == "approve_transfer_to_trading_wallet", TransferToTradingWallet.approve)
async def approving_withdraw(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    """Approving transfer to trading wallet"""
    user_data = await state.get_data()

    # TODO: Do transfer to trading wallet!

    # TODO: Make actual status
    status = 'Успешно 🎉' if True else 'Неуспешно 😬'

    await add_transfer_transaction(
        session=session,
        user_id=callback.from_user.id,
        from_wallet_id=user_data.get('from_wallet').id,
        amount=user_data.get('amount'),
    )

    await callback.message.edit_text(
        text=f"📗<b>Данные о переводе</b>:\n\n<b>Статус</b>: {status}\n\n<b>Сумма</b>: {user_data.get('amount')} USDT",
        reply_markup=new_menu_keyboard()
    )

    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "cancel_transfer_to_trading_wallet", TransferToTradingWallet.approve)
async def canceling_withdraw(callback: types.CallbackQuery, state: FSMContext):
    """Canceling transfer to trading wallet"""
    await callback.message.answer(
        text="Перевод отменен ❌",
        reply_markup=back_to_menu_keyboard()
    )

    await state.clear()
    await callback.answer()
