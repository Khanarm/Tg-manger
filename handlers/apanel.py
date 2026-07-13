from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, timedelta
from database.scheduled import create_task

from config import OWNER_ID

from userbot.client import get_all_channels

from keyboards.panel import apanel_channels_keyboard

from states.panel import PanelState


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
        reply_markup=apanel_channels_keyboard(channels)
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

    await state.clear()

    await state.update_data(
        channel_id=channel_id
    )

    await callback.message.answer(
        "📝 Send new channel name."
    )

    await state.set_state(
        PanelState.waiting_schedule_name
    )

    await callback.answer()

@router.message(PanelState.waiting_schedule_name)
async def get_schedule_name(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        name=message.text.strip()
    )

    await message.answer(
        "🔗 Send new username."
    )

    await state.set_state(
        PanelState.waiting_schedule_username
    )


@router.message(PanelState.waiting_schedule_username)
async def get_schedule_username(
    message: Message,
    state: FSMContext
):
    username = message.text.strip().replace("@", "")

    if not username:
        await message.answer(
            "❌ Please send a valid username."
        )
        return

    await state.update_data(
        username=username
    )

    await message.answer(
        "🖼 Send storage channel profile photo post link."
    )

    await state.set_state(
        PanelState.waiting_schedule_photo
    )


@router.message(PanelState.waiting_schedule_photo)
async def get_schedule_photo(
    message: Message,
    state: FSMContext
):
    if not message.text:
        await message.answer(
            "❌ Please send a valid storage channel post link."
        )
        return

    await state.update_data(
        photo_link=message.text.strip()
    )

    await message.answer(
        "📢 Forward or send the post."
    )

    await state.set_state(
        PanelState.waiting_schedule_post
    )

@router.message(PanelState.waiting_schedule_post)
async def get_schedule_post(
    message: Message,
    state: FSMContext
):
    if not message.text:
        await message.answer(
            "❌ Please send a valid storage channel post link."
        )
        return

    await state.update_data(
        post_link=message.text.strip()
    )

    builder = InlineKeyboardBuilder()

    today = datetime.now()

    for i in range(0, 31):
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
        "11:05",
        "11:10",
        "11:15",
        "11:20",
        "11:30",
        "11:35"
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

    print(data)

    if "date" not in data:
        await callback.answer(
            "❌ Session expired. Please start again.",
            show_alert=True
        )
        await state.clear()
        return

    run_at = datetime.strptime(
        f"{data['date']} {time}",
        "%Y-%m-%d %H:%M"
    )

    await create_task(
    channel_id=data["channel_id"],
    data={
        "name": data["name"],
        "username": data["username"],
        "photo_link": data["photo_link"],
        "post_link": data["post_link"],
    },
    run_at=run_at
    )

    await callback.message.edit_text(
        "✅ Automation Scheduled Successfully!\n\n"
        f"📝 Name: {data['name']}\n"
        f"🔗 Username: @{data['username']}\n"
        f"🖼 Photo: ✅\n"
        f"📢 Post: ✅\n\n"
        f"📅 Date: {run_at.strftime('%d %b %Y')}\n"
        f"🕒 Time: {time}"
    )

    await state.clear()
    await callback.answer()
