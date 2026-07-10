from userbot.client import rename_channel
from aiogram.fsm.context import FSMContext
from states.rename import RenameState

from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from userbot.client import get_channel_info

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import OWNER_ID
from userbot.client import get_all_channels
from keyboards.channels import channels_keyboard

router = Router()


@router.message(Command("setname"))
async def setname(message: Message):

    if message.from_user.id != OWNER_ID:
        await message.answer("❌ You are not authorized.")
        return

    channels = await get_all_channels()

    if not channels:
        await message.answer("❌ No channels found.")
        return

    await message.answer(
        "📢 Select a Channel",
        reply_markup=channels_keyboard(channels)
    )

async def get_channel_info(channel_id):

    client = CHANNEL_CLIENTS.get(channel_id)

    if client is None:
        return None

    entity = await client.get_entity(channel_id)

    full = await client(GetFullChannelRequest(entity))

    subscribers = full.full_chat.participants_count

    last_views = 0

    async for msg in client.iter_messages(entity, limit=1):
        last_views = msg.views or 0

    return {
        "client": client,
        "entity": entity,
        "title": entity.title,
        "subscribers": subscribers,
        "views": last_views
                                          }

@router.callback_query(lambda c: c.data.startswith("confirm_"))
async def confirm_channel(callback: CallbackQuery, state: FSMContext):

    channel_id = int(callback.data.split("_")[1])

    await state.update_data(channel_id=channel_id)

    await state.set_state(RenameState.waiting_name)

    await callback.message.edit_text(
        "✏️ Naya Channel Name bhejiye."
    )

    await callback.answer()

@router.message(RenameState.waiting_name)
async def receive_new_name(message: Message, state: FSMContext):

    data = await state.get_data()

    channel_id = data.get("channel_id")

    if not channel_id:
        await message.answer("❌ Channel not found.")
        await state.clear()
        return

    ok = await rename_channel(
        channel_id,
        message.text.strip()
    )

    if ok:
        await message.answer(
            "✅ Channel name updated successfully."
        )
    else:
        await message.answer(
            "❌ Failed to update channel name."
        )

    await state.clear()
