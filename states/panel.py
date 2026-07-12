from aiogram.fsm.state import State, StatesGroup


class PanelState(StatesGroup):
    # Normal features
    waiting_name = State()
    waiting_username = State()
    waiting_photo = State()
    waiting_bio = State()

    # Scheduled automation
    waiting_schedule_name = State()
    waiting_schedule_username = State()
    waiting_schedule_photo = State()
    waiting_schedule_post = State()
    waiting_date = State()
    waiting_time = State()

    waiting_confirm = State()
