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
