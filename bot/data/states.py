from aiogram.fsm.state import StatesGroup, State


class WithdrawOrder(StatesGroup):
    to_wallet_address = State()
    amount = State()
    approve = State()
