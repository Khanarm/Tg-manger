from telethon import TelegramClient
from telethon.sessions import StringSession

from config import API_ID, API_HASH, STRING_SESSIONS

clients = []

async def start_userbots():
    for session in STRING_SESSIONS:
        client = TelegramClient(
            StringSession(session),
            API_ID,
            API_HASH
        )

        await client.start()

        me = await client.get_me()

        print(f"Started: {me.first_name}")

        clients.append(client)
