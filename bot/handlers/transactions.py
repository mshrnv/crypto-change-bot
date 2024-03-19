from aiogram import Router, types
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import html

from bot.data.callback import DepositCallbackFactory

from bot.data.states import WithdrawOrder
from bot.keyboards.inline import deposit_keyboard, settings_keyboard
from bot.services.users import deposit, get_user_balance, withdraw
from bot.utils.crypto import create_wallet

router = Router(name="transactions")


@router.callback_query(F.data == "deposit")
async def deposit_handler(callback: types.CallbackQuery) -> None:
    """Deposit start"""
    address = create_wallet()
    await callback.message.edit_text(
        text=f"Для пополнения баланса переведите необходимую сумму в USDT по следующему адресу:\n\n{html.code(address['base58check_address'])}\n\n<b>Минимальная сумма для пополнения</b>: 5 USDT",
        reply_markup=deposit_keyboard(address['base58check_address'])
    )
    await callback.answer()


@router.callback_query(DepositCallbackFactory.filter())
async def deposit_check(
        callback: types.CallbackQuery,
        callback_data: DepositCallbackFactory,
        session: AsyncSession
):
    is_success = True
    # check for success deposit
    amount = 10
    # get amount (in USDT)

    if is_success:
        await deposit(session=session, user_id=callback.from_user.id, amount=amount, wallet=callback_data.address)
        await callback.message.edit_text(
            text=f"Успешное пополнение <b>{amount} USDT</b>",
            reply_markup=settings_keyboard()
        )
    else:
        await callback.message.edit_text(
            text="Пожалуйста, подождите, транзакция не обнаружена 🧐",
            reply_markup=settings_keyboard()
        )

    await callback.answer()


@router.callback_query(StateFilter(None), F.data == "withdraw")
async def withdraw_handler(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext) -> None:
    """Withdraw handler"""
    user_balance = await get_user_balance(session, callback.from_user.id)
    await callback.message.edit_text(
        text=f"Доступный для вывода баланс: {user_balance} USDT\n\nМинимальная сумма для вывода: 5 USDT",
        reply_markup=settings_keyboard()
    )

    await state.update_data(balance=user_balance)
    await state.set_state(WithdrawOrder.choosing_amount)
    await callback.answer()


@router.message(WithdrawOrder.choosing_amount)
async def withdraw_start(message: types.Message, session: AsyncSession, state: FSMContext) -> None:
    try:
        amount = int(message.text)
        user_data = await state.get_data()

        if amount > user_data['balance'] or amount < 5:
            raise ValueError

        wallet = create_wallet()
        print(wallet)
        # Send money to new wallet
        await withdraw(session, message.from_user.id, amount, wallet['base58check_address'])
        await message.answer(
            f"Создана траназкция по выводу {amount} USDT на внешний кошелек\nОжидайте поступления средств на следующий адрес:\n\nBase58CheckAddress: {wallet['base58check_address']}\n\nHexAddress: {wallet['hex_address']}\n\nPublic key: {wallet['public_key']}\n\nPrivate key: {wallet['private_key']}")
        await state.clear()
    except ValueError:
        await message.answer("Введите корректную сумму")
