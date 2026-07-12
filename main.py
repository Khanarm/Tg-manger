import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN

from handlers.start import router as start_router
from handlers.setname import router as setname_router
from handlers.setphoto import router as setphoto_router
from handlers.panel import router as panel_router
from handlers.apanel import router as apanel_router
from handlers.setusername import router as setusername_router

from database.mongo import db

from userbot.client import start_userbots

from automation.task_runner import task_scheduler


bot = Bot(BOT_TOKEN)

storage = MemoryStorage()

dp = Dispatcher(storage=storage)


# Routers
dp.include_router(start_router)
dp.include_router(setname_router)
dp.include_router(setusername_router)
dp.include_router(setphoto_router)
dp.include_router(panel_router)
dp.include_router(apanel_router)

async def main():

    # MongoDB check
    await db.command("ping")
    print("✅ MongoDB Connected")


    # Start Telethon userbots
    await start_userbots()


    # Start scheduled task runner
    asyncio.create_task(
        task_scheduler()
    )


    print("✅ Bot Started")


    # Start bot
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
