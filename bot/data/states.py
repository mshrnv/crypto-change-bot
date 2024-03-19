from aiogram.fsm.state import StatesGroup, State


class WithdrawOrder(StatesGroup):
    balance = State()
    choosing_amount = State()
