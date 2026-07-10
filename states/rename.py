from aiogram.fsm.state import State, StatesGroup


class RenameState(StatesGroup):
    waiting_name = State()
