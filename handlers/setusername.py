from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

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
