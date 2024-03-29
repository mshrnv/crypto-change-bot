"""Bot states"""
from aiogram.fsm.state import StatesGroup, State


class WithdrawOrder(StatesGroup):
    """Withdraw order states"""
    to_wallet_address = State()
    amount = State()
    approve = State()


class TransferToTradingWallet(StatesGroup):
    """Transferring to trading wallet state"""
    amount = State()
    approve = State()
