from telethon import TelegramClient
from telethon.tl.types import Channel
from config import API_ID, API_HASH, SESSION_NAME

client = TelegramClient(
    SESSION_NAME,
    API_ID,
    API_HASH
)


async def start_userbot():
    await client.start()


async def get_channels():
    channels = []

    async for dialog in client.iter_dialogs():
        if isinstance(dialog.entity, Channel):
            if dialog.entity.broadcast:
                channels.append(
                    {
                        "id": dialog.entity.id,
                        "title": dialog.name
                    }
                )

    return channels
