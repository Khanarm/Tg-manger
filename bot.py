from telethon import TelegramClient

from config import API_ID, API_HASH, BOT_TOKEN
from userbot.client import start_userbots

# Handlers
from handlers.start import register as start_handler
from handlers.channel import register as channel_handler
from handlers.callback import register as callback_handler
from handlers.broadcast import register as broadcast_handler


# ==========================
# BOT CLIENT
# ==========================

bot = TelegramClient(
    "manager_bot",
    API_ID,
    API_HASH
)


async def main():

    # Register Handlers
    start_handler(bot)
    channel_handler(bot)
    callback_handler(bot)
    broadcast_handler(bot)

    # Start UserBots
    await start_userbots()

    print("✅ All UserBots Started")

    # Start Bot
    await bot.start(bot_token=BOT_TOKEN)

    print("🤖 Manager Bot Started")

    await bot.run_until_disconnected()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
