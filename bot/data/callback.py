"""Callback Factories"""
from aiogram.filters.callback_data import CallbackData


class DepositWalletCallbackFactory(CallbackData, prefix="depo_wall"):
    """Deposit wallet callback factory"""
    wallet_id: int


class WithdrawWalletCallbackFactory(CallbackData, prefix="withdraw_wall"):
    """Withdraw wallet callback factory"""
    wallet_id: int


class DeleteDepositWalletCallbackFactory(CallbackData, prefix="delete_depo_wall"):
    """Delete deposit wallet callback factory"""
    wallet_id: int


class DeleteWithdrawWalletCallbackFactory(CallbackData, prefix="delete_with_draw_wall"):
    """Delete withdraw wallet callback factory"""
    wallet_id: int


class WithdrawCallbackFactory(CallbackData, prefix="wthdrw"):
    """Withdraw callback factory"""
    wallet_id: int
