import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers.start import router as start_router
from handlers.setname import router as setname_router
from userbot.client import start_userbots

bot = Bot(BOT_TOKEN)

storage = MemoryStorage()

dp = Dispatcher(storage=storage)

# Routers
dp.include_router(start_router)
dp.include_router(setname_router)


async def main():
    await start_userbots()

    print("✅ Bot Started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
