from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot.states.user import UserForm

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.set_state(UserForm.name)

    return await message.answer("What is your name?")


@router.message(UserForm.name)
async def your_name(message: Message, state: FSMContext) -> None:
    await state.set_state(UserForm.age)
    await state.update_data(name=message.text)

    return await message.answer("Good. How old are you?")


@router.message(UserForm.age)
async def your_old(message: Message, state: FSMContext) -> None:
    await state.update_data(age=message.text)

    user_data = await state.get_data()

    return await message.answer(f"Your form:\n\nName: {user_data['name']}\nAge: {user_data['age']}")
