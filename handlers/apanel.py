from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import OWNER_ID

from userbot.client import get_all_channels

from database.scheduled import create_task

from states.panel import PanelState

from datetime import datetime

from keyboards.panel import panel_channels_keyboard


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
    F.data.startswith("panel_channel_")
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
