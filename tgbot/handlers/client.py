from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.constants import CHAT_ID
from tgbot.keyboards.inline import get_confirm_or_reject_keyboard
from tgbot.states.user import UserForm

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.set_state(UserForm.name)

    return await message.answer(text="What is your name?")


@router.message(UserForm.name)
async def your_name(message: Message, state: FSMContext) -> None:
    await state.set_state(UserForm.age)
    await state.update_data(name=message.text)

    return await message.answer("Good. How old are you?")


@router.message(UserForm.age)
async def your_old(message: Message, state: FSMContext) -> None:
    await state.update_data(age=message.text)
    user_data = await state.get_data()

    return await message.answer(
        "📩 Проверьте <b>правильность</b> введённых данных:\n\n"
        f"<b>Имя:</b> {user_data['name']}\n"
        f"<b>Возраст:</b> {user_data['age']}",
        reply_markup=get_confirm_or_reject_keyboard()
    )


@router.callback_query(F.data == "confirm_data")
async def confirm_result(query: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    user_data = await state.get_data()

    await query.message.edit_text(
        text="<b>✅ Одобрено:</b> Данные успешно записаны"
    )
    await bot.send_message(
        CHAT_ID,
        f"<b>Новая заявка:</b>\n\n"
        f"<b>Имя:</b> {user_data['name']}\n"
        f"<b>Возраст:</b> {user_data['age']}"
    )
    await state.clear()


@router.callback_query(F.data == "reject_data")
async def write_rejection(query: CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    await query.message.edit_text(
        text="<b>❎ Отклонено:</b> Запись данных была отменена"
    )
    await query.answer()
