from aiogram.fsm.state import State, StatesGroup


class SetUsernameState(StatesGroup):
    waiting_username = State()
