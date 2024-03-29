"""Inline keyboards"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.data.callback import DepositWalletCallbackFactory, WithdrawWalletCallbackFactory, \
    DeleteDepositWalletCallbackFactory, DeleteWithdrawWalletCallbackFactory, WithdrawCallbackFactory, \
    TransferToTradingWalletCallbackFactory
from bot.utils.crypto import compress_address


def main_keyboard() -> InlineKeyboardMarkup:
    """Main menu"""
    buttons = [
        [InlineKeyboardButton(text="Профиль 👤", callback_data="profile")],
        [InlineKeyboardButton(text="Мои кошельки 💳", callback_data="wallets")],
        [InlineKeyboardButton(text="Настройки ⚙️", callback_data="settings")],
        [InlineKeyboardButton(text="Помощь ✉️", callback_data="support")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1, 1, 2)

    return keyboard.as_markup()


def back_to_profile_keyboard() -> InlineKeyboardMarkup:
    """Back to profile keyboard"""
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="profile")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1)

    return keyboard.as_markup()


def new_menu_keyboard() -> InlineKeyboardMarkup:
    """New menu message keyboard"""
    buttons = [
        [InlineKeyboardButton(text="Меню 📓", callback_data="new_menu")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1)

    return keyboard.as_markup()


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """Back to menu message keyboard"""
    buttons = [
        [InlineKeyboardButton(text="Меню 📓", callback_data="menu")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1)

    return keyboard.as_markup()


def profile_keyboard() -> InlineKeyboardMarkup:
    """Profile keyboard"""
    buttons = [
        [InlineKeyboardButton(text="История переводов на торговый счет 📊",
                              callback_data="history_transfer_to_trading_wallet")],
        [InlineKeyboardButton(text="История операций вывода 📁", callback_data="history_withdraw")],
        [InlineKeyboardButton(text="Мои кошельки 💳", callback_data="wallets")],
        [InlineKeyboardButton(text="Назад", callback_data="menu")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1, 1)

    return keyboard.as_markup()


def wallets_keyboard() -> InlineKeyboardMarkup:
    """Wallets categories keyboard"""
    buttons = [
        [InlineKeyboardButton(text="Торговый счет 📈", callback_data="trading_wallet")],
        [InlineKeyboardButton(text="На депозит 📥", callback_data="deposit_wallets")],
        [InlineKeyboardButton(text="На вывод 📤", callback_data="withdraw_wallets")],
        [InlineKeyboardButton(text="Назад", callback_data="menu")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1, 1, 1)

    return keyboard.as_markup()


def deposit_wallets_keyboard(wallets) -> InlineKeyboardMarkup:
    """Deposit wallets list keyboard"""
    buttons = []

    for wallet in wallets:
        buttons.append([
            InlineKeyboardButton(text=f"Кошелек ID-{wallet[0].id}: {compress_address(wallet[0].base58_address)} 💳",
                                 callback_data=DepositWalletCallbackFactory(wallet_id=wallet[0].id).pack())
        ])

    buttons.extend([
        [InlineKeyboardButton(text="Новый кошелек 🔐", callback_data="new_deposit_wallet")],
        [InlineKeyboardButton(text="Назад", callback_data="wallets")],
    ])

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1, 1)

    return keyboard.as_markup()


def withdraw_wallets_keyboard(wallets) -> InlineKeyboardMarkup:
    """Withdraw wallets list keyboards"""
    buttons = []

    for wallet in wallets:
        buttons.append([
            InlineKeyboardButton(text=f"Кошелек ID-{wallet[0].id}: {compress_address(wallet[0].base58_address)} 💳",
                                 callback_data=WithdrawWalletCallbackFactory(wallet_id=wallet[0].id).pack())
        ])

    buttons.extend([
        [InlineKeyboardButton(text="Новый кошелек 🔐", callback_data="new_withdraw_wallet")],
        [InlineKeyboardButton(text="Назад", callback_data="wallets")],
    ])

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1, 1)

    return keyboard.as_markup()


def back_to_deposit_wallets_keyboard() -> InlineKeyboardMarkup:
    """Back to deposit wallets list keyboard"""
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="deposit_wallets")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1)

    return keyboard.as_markup()


def back_to_withdraw_wallets_keyboard() -> InlineKeyboardMarkup:
    """Back to withdraw wallets list keyboard"""
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="withdraw_wallets")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1)

    return keyboard.as_markup()


def current_deposit_wallet_keyboard(wallet_id) -> InlineKeyboardMarkup:
    """Current deposit wallet keyboard"""
    # TODO: Send to trading wallet
    # TODO: Update balance
    buttons = [
        [InlineKeyboardButton(text="Перевести на торговый счет 📈",
                              callback_data=TransferToTradingWalletCallbackFactory(wallet_id=wallet_id).pack())],
        [InlineKeyboardButton(text="Обновить баланс 🔄", callback_data="update")],
        [InlineKeyboardButton(text="Удалить кошелек 🗑",
                              callback_data=DeleteDepositWalletCallbackFactory(wallet_id=wallet_id).pack())],
        [InlineKeyboardButton(text="Назад", callback_data="deposit_wallets")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1, 1, 1)

    return keyboard.as_markup()


def current_withdraw_wallet_keyboard(wallet_id) -> InlineKeyboardMarkup:
    """Current withdraw wallet keyboard"""
    # TODO: Update balance
    buttons = [
        [InlineKeyboardButton(text="Вывести на внешний кошелек 💸",
                              callback_data=WithdrawCallbackFactory(wallet_id=wallet_id).pack())],
        [InlineKeyboardButton(text="Обновить баланс 🔄", callback_data="update")],
        [InlineKeyboardButton(text="Удалить кошелек 🗑",
                              callback_data=DeleteWithdrawWalletCallbackFactory(wallet_id=wallet_id).pack())],
        [InlineKeyboardButton(text="Назад", callback_data="withdraw_wallets")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1, 1, 1, 1)

    return keyboard.as_markup()


def trading_wallet_keyboard() -> InlineKeyboardMarkup:
    """Trading wallet keyboard"""
    buttons = [
        [InlineKeyboardButton(text="История сделок на торговом счете 📖", callback_data="trading_history")],
        [InlineKeyboardButton(text="Назад", callback_data="wallets")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1, 1)

    return keyboard.as_markup()


def trading_history_keyboard() -> InlineKeyboardMarkup:
    """Trading history keyboard"""
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="trading_wallet")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1)

    return keyboard.as_markup()


def approve_withdraw_keyboard() -> InlineKeyboardMarkup:
    """Approve withdraw keyboard"""
    buttons = [
        [InlineKeyboardButton(text="Подтверждаю ✅", callback_data="approve_withdraw")],
        [InlineKeyboardButton(text="Отмена ❌", callback_data="dont_approve_withdraw")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(2)

    return keyboard.as_markup()


def approve_transfer_to_trading_wallet_keyboard() -> InlineKeyboardMarkup:
    """Approve transfer to trading wallet keyboard"""
    buttons = [
        [InlineKeyboardButton(text="Подтверждаю ✅", callback_data="approve_transfer_to_trading_wallet")],
        [InlineKeyboardButton(text="Отмена ❌", callback_data="cancel_transfer_to_trading_wallet")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(2)

    return keyboard.as_markup()


def support_keyboard() -> InlineKeyboardMarkup:
    """Support menu keyboard"""
    buttons = [
        [InlineKeyboardButton(text="Написать в поддержку 📝", callback_data="write_to_support")],
        [InlineKeyboardButton(text="Назад", callback_data="menu")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1, 1)

    return keyboard.as_markup()


def support_keyboard() -> InlineKeyboardMarkup:
    """Support menu keyboard"""
    buttons = [
        [InlineKeyboardButton(text="Написать в поддержку 📝", callback_data="write_to_support")],
        [InlineKeyboardButton(text="Назад", callback_data="menu")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1, 1)

    return keyboard.as_markup()


def write_to_support_keyboard() -> InlineKeyboardMarkup:
    """Write to support keyboard"""
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="support")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1)

    return keyboard.as_markup()


def settings_keyboard(notifications_status) -> InlineKeyboardMarkup:
    """Settings menu keyboard"""

    notifications_button_text = "Уведомления: включены ✅" if notifications_status else "Уведомления: выключены ❌"

    buttons = [
        [InlineKeyboardButton(text=notifications_button_text, callback_data="change_notifications_status")],
        [InlineKeyboardButton(text="Назад", callback_data="menu")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1, 1)

    return keyboard.as_markup()
