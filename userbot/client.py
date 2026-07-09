from telethon.sessions import StringSession

TelegramClient(
    StringSession(STRING_SESSION),
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
