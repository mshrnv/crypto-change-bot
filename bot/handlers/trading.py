"""Trading operations handlers"""
from aiogram import F
from aiogram import Router, types
from aiogram import html
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.api.crypto import get_spreads
from bot.data.callback import TransferToTradingWalletCallbackFactory, SpreadChainCallbackFactory
from bot.data.states import TransferToTradingWallet
from bot.keyboards.inline import new_menu_keyboard, approve_transfer_to_trading_wallet_keyboard, \
    back_to_menu_keyboard, trading_history_keyboard, trading_wallet_keyboard, trade_operations_keyboard, \
    chain_info_keyboard
from bot.services.transfers import add_transfer_transaction
from bot.services.wallets import get_wallet_info, get_trading_wallet_balance

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
        text=f"📗<b>Данные о переводе на торговый счет</b>:\n\n<b>Статус</b>: {status}\n\n<b>Сумма</b>: {user_data.get('amount')} USDT",
        reply_markup=new_menu_keyboard()
    )

    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "cancel_transfer_to_trading_wallet", TransferToTradingWallet.approve)
async def canceling_withdraw(callback: types.CallbackQuery, state: FSMContext):
    """Canceling transfer to trading wallet"""
    await callback.message.answer(
        text="Перевод на торговый счет отменен ❌",
        reply_markup=back_to_menu_keyboard()
    )

    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "trading_wallet")
async def trading_wallet_handler(callback: types.CallbackQuery, session: AsyncSession) -> None:
    """Trading wallet info"""
    trading_balance = await get_trading_wallet_balance(session, callback.from_user.id)
    await callback.message.edit_text(
        text=f"<b>Информация о торговом счете</b> 📈\n\n<b>Баланс</b>: {trading_balance} USDT",
        reply_markup=trading_wallet_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "trading_history")
async def trading_history_handler(callback: types.CallbackQuery, session: AsyncSession) -> None:
    """History of trading transactions"""
    # TODO: Get trading transactions history
    history = []

    history_text = "Пока не совершено ни одной сделки на торговом счете"

    if history:
        pass

    await callback.message.edit_text(
        text=f"<b>Информация о сделках на торговом счете</b> 🗂\n\n{history_text}",
        reply_markup=trading_history_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "trade_operations")
async def trade_operations_handler(callback: types.CallbackQuery, session: AsyncSession) -> None:
    """List of trading operations"""

    spreads_data = get_spreads()

    await callback.message.edit_text(
        text=f"<b>Список доступных связок</b> 📖",
        reply_markup=trade_operations_keyboard(spreads_data)
    )
    await callback.answer()


@router.callback_query(SpreadChainCallbackFactory.filter())
async def deposit_wallet_info(
        callback: types.CallbackQuery,
        callback_data: SpreadChainCallbackFactory,
        session: AsyncSession
):
    """Spread chain info"""

    spread_info = get_spreads()[callback_data.chain]

    await callback.message.edit_text(
        text=f"<b>🧩Информация о связке:</b>\n\nСвязка: {callback_data.chain}\nСпред: {spread_info['spread']}%",
        reply_markup=chain_info_keyboard()
    )
    await callback.answer()
