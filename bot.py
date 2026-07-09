import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers.start import router as start_router

from userbot.client import start_userbot

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
#dp.include_router(setname_router)
#dp.include_router(broadcast_router)


async def main():
    await start_userbot()      # Userbot start
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
