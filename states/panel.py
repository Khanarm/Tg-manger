from aiogram.fsm.state import State, StatesGroup


class PanelState(StatesGroup):
    waiting_name = State()
    waiting_username = State()
    waiting_photo = State()
    waiting_bio = State()

    # Automation
    waiting_action = State()
    waiting_value = State()
    waiting_date = State()
    waiting_time = State()
