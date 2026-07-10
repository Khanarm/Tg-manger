from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from userbot.client import update_channel_username
from states.setusername import SetUsernameState
from userbot.client import get_all_channels


router = Router()


@router.message(Command("setusername"))
async def set_username_start(message: types.Message):

    channels = await get_all_channels()

    buttons = []

    for ch in channels:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"📢 {ch.title}",
                    callback_data=f"setusername_{ch.id}"
                )
            ]
        )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    await message.answer(
        "📢 Channel select karo:",
        reply_markup=keyboard
    )


@router.callback_query(F.data.startswith("setusername_"))
async def select_channel(
    callback: types.CallbackQuery,
    state: FSMContext
):

    channel_id = int(
        callback.data.split("_")[1]
    )

    await state.update_data(
        channel_id=channel_id
    )

    await state.set_state(
        SetUsernameState.waiting_username
    )

    await callback.message.answer(
        "✅ Channel selected\n\n"
        "Ab naya username bhejo.\n"
        "Example: mychannel123"
    )

    await callback.answer()

@router.message(SetUsernameState.waiting_username)
async def receive_username(
    message: types.Message,
    state: FSMContext
):

    username = message.text.strip()

    data = await state.get_data()
    channel_id = data.get("channel_id")

    if not channel_id:
        await message.answer(
            "❌ Channel not selected"
        )
        await state.clear()
        return


    # @ remove kar do agar user ne bheja ho
    username = username.replace("@", "")


    success, result = await update_channel_username(
        channel_id,
        username
    )


    if success:
    await message.answer(
        f"✅ Username successfully changed\n\n"
        f"New username: @{username}"
    )

    await state.clear()

else:
    error = str(result)

    if "USERNAME_OCCUPIED" in error:
        msg = (
            "❌ Ye username already kisi aur ne le rakha hai.\n\n"
            "Kripya koi dusra username bhejo."
        )

    elif "USERNAME_INVALID" in error:
        msg = (
            "❌ Invalid username.\n\n"
            "Username rules:\n"
            "• 5-32 characters\n"
            "• Sirf a-z, 0-9 aur underscore (_)\n"
            "• Space allowed nahi hai\n\n"
            "Naya username bhejo."
        )

    else:
        msg = (
            f"❌ Username change failed\n\n"
            f"{error}\n\n"
            "Naya username try karo."
        )

    await message.answer(msg)

    # state clear nahi karenge
