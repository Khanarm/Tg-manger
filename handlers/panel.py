from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from config import OWNER_ID
from userbot.client import get_all_channels, get_channel_info
from keyboards.panel import (
    panel_channels_keyboard,
    channel_info_keyboard,
)

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
        
@router.message(Command("hello"))
async def hello(message: Message):
    await message.answer("Hello Working")
    
    
        
