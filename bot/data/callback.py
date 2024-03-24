from aiogram.filters.callback_data import CallbackData


class DepositWalletCallbackFactory(CallbackData, prefix="depo_wall"):
    wallet_id: int


class WithdrawWalletCallbackFactory(CallbackData, prefix="withdraw_wall"):
    wallet_id: int


class DeleteDepositWalletCallbackFactory(CallbackData, prefix="delete_depo_wall"):
    wallet_id: int


class DeleteWithdrawWalletCallbackFactory(CallbackData, prefix="delete_with_draw_wall"):
    wallet_id: int


class WithdrawCallbackFactory(CallbackData, prefix="wthdrw"):
    wallet_id: int
