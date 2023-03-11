from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select

from tgbot.constants import CHAT_ID, ADM_ID
from tgbot.database import Currency
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
        f"<b>Возраст:</b> {user_data['age']}\n",
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


async def check_currency(number: int) -> bool:
    for i in number:
        if i == ",":
            return False
        else:
            return True


@router.message(Command(commands=["add_curr"]))
async def exchange_rates(message: Message, command: CommandObject, session_maker):
    if message.from_user.id == ADM_ID and command.args:
        await message.answer("<b>✅ Одобрено:</b> Курс успешно изменен")

        async with session_maker() as session:
            async with session.begin():
                await session.merge(
                    Currency(
                        adm_id=ADM_ID,
                        yuan=int(command.args)
                    )
                )
                await session.commit()
    else:
        await message.answer("<b>❎ Отклонено:</b> У вас нет доступа к этой комнаде")


@router.message(Command(commands=["exchange"]))
async def get_exchange(message: Message, session_maker):
    async with session_maker() as session:
        async with session.begin():
            data = await session.execute(select(Currency).where(Currency.adm_id == ADM_ID))
            data1 = data.first()
            await session.commit()

    await message.answer(f"Текущий курс: {data1.Currency.yuan}")
