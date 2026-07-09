from telethon import TelegramClient
from config import API_ID, API_HASH, SESSION_NAME

client = TelegramClient(
    SESSION_NAME,
    API_ID,
    API_HASH
)


async def start_userbot():
    await client.start()
    me = await client.get_me()
    print(f"✅ Userbot Connected : {me.first_name} (@{me.username})")
