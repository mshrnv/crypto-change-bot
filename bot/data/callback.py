from aiogram.filters.callback_data import CallbackData


class DepositCallbackFactory(CallbackData, prefix="deposit"):
    address: str
