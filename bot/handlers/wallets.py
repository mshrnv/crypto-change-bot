from aiogram import Router, types
from aiogram import F
from aiogram import html
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.api.tron import transfer_usdt
from bot.data.callback import DeleteDepositWalletCallbackFactory, \
    DeleteWithdrawWalletCallbackFactory, DepositWalletCallbackFactory, WithdrawWalletCallbackFactory, \
    WithdrawCallbackFactory
from bot.data.states import WithdrawOrder

from bot.keyboards.inline import back_to_deposit_wallets_keyboard, \
    deposit_wallets_keyboard, wallets_keyboard, current_deposit_wallet_keyboard, withdraw_wallets_keyboard, \
    back_to_withdraw_wallets_keyboard, current_withdraw_wallet_keyboard, trading_wallet_keyboard, \
    trading_history_keyboard, approve_withdraw_keyboard, new_menu_keyboard
from bot.services.wallets import get_user_wallets, get_wallet_info, delete_wallet, add_wallet, \
    get_trading_wallet_balance
from bot.utils.crypto import create_wallet, check_address

router = Router(name="wallets")


@router.callback_query(F.data == "wallets")
async def wallets_handler(callback: types.CallbackQuery) -> None:
    """Wallets"""
    await callback.message.edit_text(
        text="Выберите категорию",
        reply_markup=wallets_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "deposit_wallets")
async def deposit_wallets_handler(callback: types.CallbackQuery, session: AsyncSession) -> None:
    """Deposit wallets"""
    wallets = await get_user_wallets(session=session, user_id=callback.from_user.id, is_deposit=True)
    await callback.message.edit_text(
        text="Список кошельков для пополнения",
        reply_markup=deposit_wallets_keyboard(wallets)
    )
    await callback.answer()


@router.callback_query(F.data == "withdraw_wallets")
async def withdraw_wallets_handler(callback: types.CallbackQuery, session: AsyncSession) -> None:
    """Withdraw wallets"""
    wallets = await get_user_wallets(session=session, user_id=callback.from_user.id, is_deposit=False)
    await callback.message.edit_text(
        text="Список кошельков для вывода",
        reply_markup=withdraw_wallets_keyboard(wallets)
    )
    await callback.answer()


@router.callback_query(F.data == "new_deposit_wallet")
async def new_deposit_wallet_handler(callback: types.CallbackQuery, session: AsyncSession) -> None:
    """New Deposit wallet"""
    wallet = create_wallet()
    await add_wallet(session, callback.from_user.id, True, wallet)
    # TODO: Add wallet info into message
    await callback.message.edit_text(
        text="Кошелек успешно добавлен",
        reply_markup=back_to_deposit_wallets_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "new_withdraw_wallet")
async def new_withdraw_wallet_handler(callback: types.CallbackQuery, session: AsyncSession) -> None:
    """New Withdraw wallet"""
    wallet = create_wallet()
    await add_wallet(session, callback.from_user.id, False, wallet)
    # TODO: Add wallet info into message
    await callback.message.edit_text(
        text="Кошелек успешно добавлен",
        reply_markup=back_to_withdraw_wallets_keyboard()
    )
    await callback.answer()


@router.callback_query(DepositWalletCallbackFactory.filter())
async def deposit_wallet_info(
        callback: types.CallbackQuery,
        callback_data: DepositWalletCallbackFactory,
        session: AsyncSession
):
    wallet_info = await get_wallet_info(session=session, wallet_id=callback_data.wallet_id)
    await callback.message.edit_text(
        text=f"<b>Информация о кошельке:</b>\n\nHexAddress: {html.pre(wallet_info.hex_address)}\n\nBase58Address: {html.pre(wallet_info.base58_address)}\n\n<b>Баланс</b>: {wallet_info.balance} USDT",
        reply_markup=current_deposit_wallet_keyboard(wallet_info.id)
    )
    await callback.answer()


@router.callback_query(WithdrawWalletCallbackFactory.filter())
async def withdraw_wallet_info(
        callback: types.CallbackQuery,
        callback_data: WithdrawWalletCallbackFactory,
        session: AsyncSession
):
    wallet_info = await get_wallet_info(session=session, wallet_id=callback_data.wallet_id)
    await callback.message.edit_text(
        text=f"<b>Информация о кошельке:</b>\n\nHexAddress: {html.pre(wallet_info.hex_address)}\n\nBase58Address: {html.pre(wallet_info.base58_address)}\n\n<b>Баланс</b>: {wallet_info.balance} USDT",
        reply_markup=current_withdraw_wallet_keyboard(wallet_info.id)
    )
    await callback.answer()


@router.callback_query(DeleteDepositWalletCallbackFactory.filter())
async def delete_deposit_wallet(
        callback: types.CallbackQuery,
        callback_data: DeleteDepositWalletCallbackFactory,
        session: AsyncSession
):
    await delete_wallet(session, callback_data.wallet_id)
    # TODO: Add wallet address to CallbackFactory
    await callback.message.edit_text(
        text="Кошелек успешно удален",
        reply_markup=back_to_deposit_wallets_keyboard()
    )
    await callback.answer()


@router.callback_query(DeleteWithdrawWalletCallbackFactory.filter())
async def delete_withdraw_wallet(
        callback: types.CallbackQuery,
        callback_data: DeleteDepositWalletCallbackFactory,
        session: AsyncSession
):
    await delete_wallet(session, callback_data.wallet_id)
    # TODO: Add wallet address to CallbackFactory
    await callback.message.edit_text(
        text="Кошелек успешно удален",
        reply_markup=back_to_withdraw_wallets_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "trading_wallet")
async def trading_wallet_handler(callback: types.CallbackQuery, session: AsyncSession) -> None:
    """Trading wallet"""
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


@router.callback_query(WithdrawCallbackFactory.filter())
async def address_withdraw_wallet(
        callback: types.CallbackQuery,
        callback_data: WithdrawCallbackFactory,
        session: AsyncSession,
        state: FSMContext
):
    await callback.message.edit_text(
        text="Введите адрес кошелька на который необходимо вывести активы 💸",
    )

    # TODO: FRom wallet id from callback factory

    from_wallet = await get_wallet_info(session, callback_data.wallet_id)
    await state.update_data(from_wallet=from_wallet)
    await state.set_state(WithdrawOrder.to_wallet_address)
    await callback.answer()


@router.message(WithdrawOrder.to_wallet_address)
async def to_address_withdraw_wallet(message: types.Message, state: FSMContext):
    if check_address(message.text):
        await state.update_data(to_address=message.text)
        await message.answer(
            text="Укажите сумму перевода в USDT 💵",
        )
        await state.set_state(WithdrawOrder.amount)
    else:
        await message.answer(
            text="Неверно введен адрес кошелька для вывода, попробуйте еще раз 🔄",
        )


@router.message(WithdrawOrder.amount)
async def amount_withdraw_wallet(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        # TODO: Check balance!
        await state.update_data(amount=amount)

        user_data = await state.get_data()
        print(user_data)
        await message.answer(
            text=f"🧾<b>Подтвердите данные транзакции</b>:\n\nКошелек-источник (ID-{user_data.get('from_wallet').id}):\n{html.pre(user_data.get('from_wallet').base58_address)}\n\nАдрес перевода:\n{html.pre(user_data.get('to_address'))}\n\nСумма перевода:\n{user_data.get('amount')} USDT\n\nВы уверены, что хотите совершить транзакцию?",
            reply_markup=approve_withdraw_keyboard()
        )

        await state.set_state(WithdrawOrder.approve)
    except ValueError:
        await message.answer(
            text="Неверно введена сумма для перевода, попробуйте еще раз 🔄"
        )

@router.callback_query(F.data == "approve_withdraw", WithdrawOrder.approve)
async def amount_withdraw_wallet(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    # TODO: Save to DB
    result = await transfer_usdt(user_data.get('from_wallet').base58_address, user_data.get('to_address'), user_data.get('amount'), user_data.get('from_wallet').private_key)

    status = 'Успешно 🎉' if result['result'] else 'Неуспешно 😬'
    trx_id = result.get('txid') if result.get('txid') else 'Ошибка'

    await callback.message.edit_text(
        text=f"📗<b>Данные о транзакции</b>:\n\n<b>Статус</b>: {status}\n\n<b>Transaction ID</b>:\n{html.pre(trx_id)}",
        reply_markup=new_menu_keyboard()
    )

    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "dont_approve_withdraw", WithdrawOrder.approve)
async def amount_withdraw_wallet(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Транзакция отменена ❌",
        reply_markup=new_menu_keyboard()
    )
    await state.clear()
    await callback.answer()

# @router.callback_query(F.data == "withdraw")
# async def withdraw_handler(callback: types.CallbackQuery, session: AsyncSession) -> None:
#     """Withdraw"""
#
#     wallet = await get_wallet_info(session, 1)
#     wallet2 = await get_wallet_info(session, 2)
#
#     result = await transfer_usdt(wallet.base58_address, wallet2.base58_address, 100, wallet.private_key)
#
#     await callback.message.edit_text(
#         text=f"{result}",
#     )
#     await callback.answer()
