from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from userbot.client import get_channels

router = Router()


@router.message(Command("channels"))
async def channels(message: Message):

    channels = await get_channels()

    keyboard = []

    for channel in channels:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=channel["title"],
                    callback_data=f"channel_{channel['id']}"
                )
            ]
        )

    await message.answer(
        "📢 Select Channel",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
                      )
