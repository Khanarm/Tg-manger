from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("setusername"))
async def set_username_start(message: types.Message):
    await message.answer(
        "📢 Username change system\n\n"
        "Pehle channel select karo jiska username change karna hai."
    )
