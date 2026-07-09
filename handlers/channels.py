from aiogram.types import CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetHistoryRequest

from userbot.client import client, get_channels

router = Router()


@router.message(Command("channels"))
async def channels(message: Message):

    keyboard = []

    for ch in await get_channels():
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=ch["title"],
                    callback_data=f"channel:{ch['id']}"
                )
            ]
        )

    await message.answer(
        "📢 Select Channel",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )


@router.callback_query(F.data.startswith("channel:"))
async def channel_info(callback: CallbackQuery):

    channel_id = int(callback.data.split(":")[1])

    entity = await client.get_entity(channel_id)

    full = await client(GetFullChannelRequest(entity))

    members = full.full_chat.participants_count

    history = await client(
        GetHistoryRequest(
            peer=entity,
            limit=1,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0,
        )
    )

    views = 0

    if history.messages:
        views = history.messages[0].views or 0

    text = f"""
📢 <b>{entity.title}</b>

👥 Subscribers : <code>{members}</code>

👀 Last Post Views : <code>{views}</code>
"""

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Confirm",
                    callback_data=f"confirm:{channel_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅ Back",
                    callback_data="back_channels"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        text,
        reply_markup=kb
    )

    await callback.answer()

@router.callback_query(F.data.startswith("channel_"))
async def channel_info(callback: CallbackQuery):

    channel_id = int(callback.data.split("_")[1])

    entity = await client.get_entity(channel_id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Confirm",
                    callback_data=f"confirm_{channel_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅ Back",
                    callback_data="back_channels"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        f"📢 {entity.title}\n\n🆔 {channel_id}",
        reply_markup=keyboard
    )

    await callback.answer()
