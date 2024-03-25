"""Bot states"""
from aiogram.fsm.state import StatesGroup, State


class WithdrawOrder(StatesGroup):
    """Withdraw order states"""
    to_wallet_address = State()
    amount = State()
    approve = State()
