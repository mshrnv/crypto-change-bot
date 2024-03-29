"""Callback Factories"""
from aiogram.filters.callback_data import CallbackData


class DepositWalletCallbackFactory(CallbackData, prefix="dpst_wall"):
    """Deposit wallet callback factory"""
    wallet_id: int


class WithdrawWalletCallbackFactory(CallbackData, prefix="wthdrw_wall"):
    """Withdraw wallet callback factory"""
    wallet_id: int


class DeleteDepositWalletCallbackFactory(CallbackData, prefix="delete_dpst_wall"):
    """Delete deposit wallet callback factory"""
    wallet_id: int


class DeleteWithdrawWalletCallbackFactory(CallbackData, prefix="delete_wthdrw_wall"):
    """Delete withdraw wallet callback factory"""
    wallet_id: int


class WithdrawCallbackFactory(CallbackData, prefix="wthdrw"):
    """Withdraw callback factory"""
    wallet_id: int


class TransferToTradingWalletCallbackFactory(CallbackData, prefix="trnsfr_to_trdng"):
    """Transfer to trading wallet callback factory"""
    wallet_id: int
