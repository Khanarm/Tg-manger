from aiogram.fsm.state import StatesGroup, State


class PanelStates(StatesGroup):
    waiting_name = State()
    waiting_username = State()
    waiting_photo = State()
    waiting_bio = State()
