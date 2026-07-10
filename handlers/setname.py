from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from config import OWNER_ID
from keyboards.channels import channels_keyboard
from states.rename import RenameState

from userbot.client import (
    get_all_channels,
    get_channel_info,
    rename_channel,
)

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
        await message.answer("✅ Channel name updated successfully.")
    else:
        await message.answer("❌ Failed to update channel name.")

    await state.clear()


@router.callback_query(lambda c: c.data.startswith("channel_"))
async def open_channel(callback: CallbackQuery):

    channel_id = int(callback.data.split("_")[1])

    data = await get_channel_info(channel_id)

    if data is None:
        await callback.answer(
            "❌ Channel not found.",
            show_alert=True
        )
        return

    kb = InlineKeyboardBuilder()

    kb.button(
        text="✅ Confirm",
        callback_data=f"confirm_{channel_id}"
    )

    kb.button(
        text="⬅️ Back",
        callback_data="back_channels"
    )

    kb.adjust(2)

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
        reply_markup=kb.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()


@router.callback_query(lambda c: c.data == "back_channels")
async def back_channels(callback: CallbackQuery):

    channels = await get_all_channels()

    await callback.message.edit_text(
        "📢 Select a Channel",
        reply_markup=channels_keyboard(channels)
    )

    await callback.answer()
