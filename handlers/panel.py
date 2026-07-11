from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import OWNER_ID
from userbot.client import get_all_channels
from keyboards.panel import panel_channels_keyboard

router = Router()


@router.message(Command("panel"))
async def panel(message: Message):

    if message.from_user.id != OWNER_ID:
        await message.answer("❌ You are not authorized.")
        return

    channels = await get_all_channels()

    if not channels:
        await message.answer("❌ No channels found.")
        return

    await message.answer(
        "📋 Select a Channel",
        reply_markup=panel_channels_keyboard(channels)
    )

@router.callback_query(F.data.startswith("panel_channel_"))
async def open_channel(callback: CallbackQuery):

    channel_id = int(callback.data.split("_")[2])

    data = await get_channel_info(channel_id)

    if data is None:
        await callback.answer(
            "❌ Channel not found",
            show_alert=True
        )
        return

    username = (
        f"@{data['username']}"
        if data["username"]
        else "No Username"
    )

    text = (
        f"📢 <b>{data['title']}</b>\n\n"
        f"👤 Username: <b>{username}</b>\n"
        f"👥 Subscribers: <b>{data['subscribers']}</b>\n"
        f"👁 Last Post Views: <b>{data['views']}</b>"
    )

    await callback.message.edit_text(
        text,
        reply_markup=channel_info_keyboard(channel_id),
        parse_mode="HTML"
    )

    await callback.answer()
    
@router.message(Command("hello"))
async def hello(message: Message):
    await message.answer("Hello Working")
