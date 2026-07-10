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
