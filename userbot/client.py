from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import Channel

from config import API_ID, API_HASH, STRING_SESSIONS

clients = []

# channel_id -> client
CHANNEL_CLIENTS = {}

async def start_userbots():
    for session in STRING_SESSIONS:
        client = TelegramClient(
            StringSession(session),
            API_ID,
            API_HASH
        )

        await client.start()

        me = await client.get_me()
        print(f"Started : {me.first_name}")

        clients.append(client)


async def get_all_channels():

    CHANNEL_CLIENTS.clear()

    channels = []

    for client in clients:

        async for dialog in client.iter_dialogs():

            if not dialog.is_channel:
                continue

            entity = dialog.entity

            if not isinstance(entity, Channel):
                continue

            channels.append(entity)

            CHANNEL_CLIENTS[entity.id] = client

    return channels
