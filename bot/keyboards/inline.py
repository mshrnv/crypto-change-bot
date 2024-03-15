from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_keyboard() -> InlineKeyboardMarkup:
    """Use in main menu."""
    buttons = [
        [InlineKeyboardButton(text="Профиль 👤", callback_data="profile")],
        [InlineKeyboardButton(text="Пополнить 💳", callback_data="deposit")],
        [InlineKeyboardButton(text="Вывести 💸", callback_data="withdraw")],
        [InlineKeyboardButton(text="Настройки ⚙️", callback_data="settings")],
        [InlineKeyboardButton(text="Помощь ✉️", callback_data="support")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1, 2, 2)

    return keyboard.as_markup()


def profile_keyboard() -> InlineKeyboardMarkup:
    """Use in profile menu."""
    buttons = [
        [InlineKeyboardButton(text="История транзакций 📖", callback_data="history")],
        [InlineKeyboardButton(text="Пополнить 💳", callback_data="deposit")],
        [InlineKeyboardButton(text="Вывести 💸", callback_data="withdraw")],
        [InlineKeyboardButton(text="Назад", callback_data="menu")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1, 2, 1)

    return keyboard.as_markup()


def support_keyboard() -> InlineKeyboardMarkup:
    """Support menu"""
    buttons = [
        [InlineKeyboardButton(text="Написать в поддержку 📝", callback_data="write")],
        [InlineKeyboardButton(text="Назад", callback_data="menu")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1, 1)

    return keyboard.as_markup()


def history_keyboard() -> InlineKeyboardMarkup:
    """Support menu"""
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="profile")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1)

    return keyboard.as_markup()


def settings_keyboard() -> InlineKeyboardMarkup:
    """Support menu"""
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="menu")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1)

    return keyboard.as_markup()
