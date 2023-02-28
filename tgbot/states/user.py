"""
This file is responsible for using FSM
"""

from aiogram.fsm.state import State, StatesGroup


class UserForm(StatesGroup):
    name = State()
    age = State()
    check = State()