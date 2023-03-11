"""
This file is responsible for using FSM
"""

from aiogram.fsm.state import State, StatesGroup


class UserForm(StatesGroup):
    name = State()
    age = State()
    photo = State()
    photo_id = State()
    check = State()