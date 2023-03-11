from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_confirm_or_reject_keyboard():
    menu_builder = InlineKeyboardBuilder()

    menu_builder.row(
        InlineKeyboardButton(text="✅", callback_data="confirm_data"),
        InlineKeyboardButton(text="❎", callback_data="reject_data"),
    )

    return menu_builder.as_markup()


def get_refresh_button():
    builder = InlineKeyboardBuilder()

    builder.button(text="🔄 Обновить", callback_data="refresh_data")

    builder.adjust(1)
    return builder.as_markup()
