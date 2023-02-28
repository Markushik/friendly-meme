from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_confirm_or_reject_keyboard():
    menu_builder = InlineKeyboardBuilder()

    menu_builder.row(
        InlineKeyboardButton(text="✅", callback_data="confirm_data"),
        InlineKeyboardButton(text="❎", callback_data="reject_data"),
    )

    return menu_builder.as_markup()
