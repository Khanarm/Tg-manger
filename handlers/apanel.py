from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, timedelta
from database.scheduled import create_task

from config import OWNER_ID

from userbot.client import get_all_channels

from database.scheduled import create_task

from states.panel import PanelState

from datetime import datetime

from keyboards.panel import apanel_channels_keyboard


router = Router()


@router.message(Command("apanel"))
async def apanel(message: Message):

    if message.from_user.id != OWNER_ID:
        await message.answer(
            "❌ You are not authorized."
        )
        return


    channels = await get_all_channels()


    if not channels:
        await message.answer(
            "❌ No channels found."
        )
        return


    await message.answer(
        "📋 Select Channel for Automation",
        reply_markup=panel_channels_keyboard(channels)
    )



@router.callback_query(
    F.data.startswith("apanel_channel_")
)
async def auto_select_channel(
    callback: CallbackQuery,
    state: FSMContext
):

    channel_id = int(
        callback.data.split("_")[2]
    )


    await state.update_data(
        channel_id=channel_id
    )


    await callback.message.answer(
        "⚙️ Select Action:\n\n"
        "📝 name\n"
        "👤 username\n"
        "🖼 photo\n"
        "📢 post\n\n"
        "Example send:\n"
        "name"
    )


    await state.set_state(
        PanelState.waiting_action
    )


    await callback.answer()

@router.message(PanelState.waiting_action)
async def get_action(
    message: Message,
    state: FSMContext
):

    action = message.text.lower().strip()

    if action not in [
        "name",
        "username",
        "photo",
        "post"
    ]:
        await message.answer(
            "❌ Invalid action\n\n"
            "Use:\n"
            "name\n"
            "username\n"
            "photo\n"
            "post"
        )
        return


    await state.update_data(
        action=action
    )


    await message.answer(
        "📝 Ab value bhejo.\n\n"
        "Example:\n"
        "Movie Hub\n"
        "moviehub\n"
        "photo path"
    )


    await state.set_state(
        PanelState.waiting_value
    )

@router.message(PanelState.waiting_value)
async def get_value(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        value=message.text
    )

    builder = InlineKeyboardBuilder()

    today = datetime.now()

    for i in range(1, 8):
        date = today + timedelta(days=i)

        builder.button(
            text=date.strftime("%d %b"),
            callback_data=f"auto_date_{date.strftime('%Y-%m-%d')}"
        )

    builder.adjust(2)

    await message.answer(
        "📅 Select Date",
        reply_markup=builder.as_markup()
    )


    await state.set_state(
        PanelState.waiting_date
)

@router.callback_query(
    F.data.startswith("auto_date_")
)
async def select_date(
    callback: CallbackQuery,
    state: FSMContext
):

    date = callback.data.replace(
        "auto_date_",
        ""
    )

    await state.update_data(
        date=date
    )


    builder = InlineKeyboardBuilder()

    times = [
        "09:00",
        "10:00",
        "12:00",
        "15:00",
        "18:00",
        "21:00"
    ]


    for t in times:

        builder.button(
            text=t,
            callback_data=f"auto_time_{t}"
        )


    builder.adjust(3)


    await callback.message.edit_text(
        "⏰ Select Time",
        reply_markup=builder.as_markup()
    )


    await state.set_state(
        PanelState.waiting_time
    )

    await callback.answer()

@router.callback_query(
    F.data.startswith("auto_time_")
)
async def select_time(
    callback: CallbackQuery,
    state: FSMContext
):

    time = callback.data.replace(
        "auto_time_",
        ""
    )


    data = await state.get_data()


    run_at = datetime.strptime(
        f"{data['date']} {time}",
        "%Y-%m-%d %H:%M"
    )


    await create_task(
        channel_id=data["channel_id"],
        action=data["action"],
        data={
            data["action"]: data["value"]
        },
        run_at=run_at
    )


    await callback.message.edit_text(
        "✅ Scheduled successfully.\n\n"
        f"📅 {run_at.strftime('%d %b %Y')}\n"
        f"⏰ {time}"
    )


    await state.clear()

    await callback.answer()
