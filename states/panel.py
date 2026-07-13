from aiogram.fsm.state import StatesGroup, State


class PanelState(StatesGroup):

    # Normal Panel
    waiting_name = State()
    waiting_username = State()
    waiting_post = State()

    # Automation Panel
    waiting_schedule_name = State()
    waiting_schedule_username = State()
    waiting_schedule_photo = State()
    waiting_schedule_post = State()
    waiting_post_link = State()

    waiting_date = State()
    waiting_time = State()

print("WAITING POST EXISTS:", hasattr(PanelState, "waiting_post"))
