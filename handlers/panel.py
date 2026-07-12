from aiogram import Router, F
from states.panel import PanelState
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
import os
import tempfile

from userbot.client import send_channel_post

from config import OWNER_ID

from userbot.client import (
    get_all_channels,
    get_channel_info,
)

from keyboards.panel import (
    panel_channels_keyboard,
    channel_info_keyboard,
    edit_menu_keyboard,
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
    )


@router.callback_query(F.data == "panel_back_channels")
async def back_channels(callback: CallbackQuery):

    channels = await get_all_channels()

    await callback.message.edit_text(
        "📋 Select a Channel",
        reply_markup=panel_channels_keyboard(channels)
    )

    await callback.answer()


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
        f"👤 Username : <b>{username}</b>\n"
        f"👥 Subscribers : <b>{data['subscribers']}</b>\n"
        f"👁 Last Post Views : <b>{data['views']}</b>"
    )

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=channel_info_keyboard(channel_id)
    )

    await callback.answer()


@router.callback_query(F.data.startswith("panel_edit_"))
async def edit_menu(callback: CallbackQuery):

    channel_id = int(callback.data.split("_")[2])

    await callback.message.edit_text(
        "⚙️ <b>Edit Menu</b>\n\nChoose an option.",
        parse_mode="HTML",
        reply_markup=edit_menu_keyboard(channel_id)
    )

    await callback.answer()

# ---------- PART 1 END ----------
# ---------- PART 2 START ----------

from aiogram.fsm.context import FSMContext
from states.panel import PanelState

from userbot.client import (
    rename_channel,
    update_channel_username,
)


@router.callback_query(F.data.startswith("panel_name_"))
async def panel_change_name(callback: CallbackQuery, state: FSMContext):

    channel_id = int(callback.data.split("_")[2])

    await state.update_data(channel_id=channel_id)
    await state.set_state(PanelState.waiting_name)

    await callback.message.edit_text(
        "📝 Send new channel name."
    )

    await callback.answer()


@router.message(PanelState.waiting_name)
async def receive_new_name(message: Message, state: FSMContext):

    data = await state.get_data()
    channel_id = data["channel_id"]

    ok = await rename_channel(
        channel_id,
        message.text.strip()
    )

    if ok:
        await message.answer("✅ Channel name updated.")
    else:
        await message.answer("❌ Failed to update channel name.")

    info = await get_channel_info(channel_id)

    username = (
        f"@{info['username']}"
        if info["username"]
        else "No Username"
    )

    await message.answer(
        f"⚙️ <b>Edit Menu</b>\n\n"
        f"📢 {info['title']}\n"
        f"👤 {username}",
        parse_mode="HTML",
        reply_markup=edit_menu_keyboard(channel_id)
    )

    await state.clear()


@router.callback_query(F.data.startswith("panel_username_"))
async def panel_change_username(callback: CallbackQuery, state: FSMContext):

    channel_id = int(callback.data.split("_")[2])

    await state.update_data(channel_id=channel_id)
    await state.set_state(PanelState.waiting_username)

    await callback.message.edit_text(
        "👤 Send new username.\n\nExample:\nmychannel123"
    )

    await callback.answer()


@router.message(PanelState.waiting_username)
async def receive_username(message: Message, state: FSMContext):

    data = await state.get_data()

    channel_id = data["channel_id"]

    username = message.text.replace("@", "").strip()

    success, result = await update_channel_username(
        channel_id,
        username
    )

    if success:

        await message.answer("✅ Username updated.")

        info = await get_channel_info(channel_id)

        username = (
            f"@{info['username']}"
            if info["username"]
            else "No Username"
        )

        await message.answer(
            f"⚙️ <b>Edit Menu</b>\n\n"
            f"📢 {info['title']}\n"
            f"👤 {username}",
            parse_mode="HTML",
            reply_markup=edit_menu_keyboard(channel_id)
        )

        await state.clear()

    else:

        if "USERNAME_OCCUPIED" in str(result):

            await message.answer(
                "❌ Username already taken.\n\nSend another username."
            )

        elif "USERNAME_INVALID" in str(result):

            await message.answer(
                "❌ Invalid username.\n\nSend another username."
            )

        else:

            await message.answer(
                f"❌ {result}\n\nTry again."
            )

# ---------- PART 2 END ----------
@router.callback_query(F.data.startswith("panel_post_"))
async def panel_post(callback: CallbackQuery, state: FSMContext):

    channel_id = int(callback.data.split("_")[2])

    await state.update_data(channel_id=channel_id)
    await state.set_state(PanelState.waiting_post)

    await callback.message.edit_text(
        "📝 <b>Send the post you want to publish.</b>\n\n"
        "Supported:\n"
        "• Text\n"
        "• Photo\n"
        "• Video\n"
        "• Document\n"
        "• Audio\n"
        "• Animation\n\n"
        "Send any one message now.",
        parse_mode="HTML"
    )

    await callback.answer()

@router.message(PanelState.waiting_post, F.text)
async def receive_text_post(message: Message, state: FSMContext):

    data = await state.get_data()
    channel_id = data["channel_id"]

    success, result = await send_channel_post(
        channel_id=channel_id,
        text=message.text,
    )

    if success:

        await message.answer(
            "✅ Post published successfully."
        )

        info = await get_channel_info(channel_id)

        username = (
            f"@{info['username']}"
            if info["username"]
            else "No Username"
        )

        @router.message(PanelState.waiting_post, F.text)
async def receive_text_post(message: Message, state: FSMContext):

    data = await state.get_data()
    channel_id = data["channel_id"]

    success, result = await send_channel_post(
        channel_id=channel_id,
        text=message.text,
    )

    if success:

        await message.answer(
            "✅ Post published successfully."
        )

        info = await get_channel_info(channel_id)

        username = (
            f"@{info['username']}"
            if info["username"]
            else "No Username"
        )
        @router.message(PanelState.waiting_post, F.text)
async def receive_text_post(message: Message, state: FSMContext):

    data = await state.get_data()
    channel_id = data["channel_id"]

    success, result = await send_channel_post(
        channel_id=channel_id,
        text=message.text,
    )

    if success:

        await message.answer(
            "✅ Post published successfully."
        )

        info = await get_channel_info(channel_id)

        username = (
            f"@{info['username']}"
            if info["username"]
            else "No Username"
        )
        @router.message(PanelState.waiting_post, F.text)
async def receive_text_post(message: Message, state: FSMContext):

    data = await state.get_data()
    channel_id = data["channel_id"]

    success, result = await send_channel_post(
        channel_id=channel_id,
        text=message.text,
    )

    if success:

        await message.answer(
            "✅ Post published successfully."
        )

        info = await get_channel_info(channel_id)

        username = (
            f"@{info['username']}"
            if info["username"]
            else "No Username"
        )
