from aiogram.fsm.state import State, StatesGroup


class SetPhotoState(StatesGroup):
    waiting_photo = State()
