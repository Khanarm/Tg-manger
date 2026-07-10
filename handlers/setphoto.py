from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from userbot.client import get_all_channels, update_channel_photo
from states.setphoto import SetPhotoState


router = Router()


@router.message(Command("setphoto"))
async def set_photo_start(message: types.Message):

    channels = await get_all_channels()

    buttons = []

    for ch in channels:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"📢 {ch.title}",
                    callback_data=f"setphoto_{ch.id}"
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


@router.callback_query(F.data.startswith("setphoto_"))
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
        SetPhotoState.waiting_photo
    )

    await callback.message.answer(
        "✅ Channel selected\n\n"
        "Ab channel ka naya profile photo bhejo."
    )

    await callback.answer()


@router.message(
    SetPhotoState.waiting_photo,
    F.photo
)
async def receive_photo(
    message: types.Message,
    state: FSMContext
):

    data = await state.get_data()

    channel_id = data.get("channel_id")

    if not channel_id:
        await message.answer(
            "❌ Channel not selected"
        )
        await state.clear()
        return


    photo = message.photo[-1]

    file = await message.bot.get_file(
        photo.file_id
    )

    photo_path = "channel_photo.jpg"

    await message.bot.download_file(
        file.file_path,
        photo_path
    )


    success, result = await update_channel_photo(
        channel_id,
        photo_path
    )


    if success:
        await message.answer(
            "✅ Channel profile photo successfully changed."
        )

    else:
        await message.answer(
            f"❌ Photo change failed\n\n{result}"
        )


    await state.clear()
