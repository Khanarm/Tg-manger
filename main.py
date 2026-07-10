import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers.start import router
from userbot.client import start_userbots
from handlers.setname import router as setname_router

bot = Bot(BOT_TOKEN)

dp = Dispatcher()

dp.include_router(router)

async def main():
    await start_userbots()

    print("Bot Started")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
