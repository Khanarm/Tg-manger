from telethon.tl.functions.channels import EditTitleRequest

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import Channel
from telethon.tl.functions.channels import GetFullChannelRequest

from config import API_ID, API_HASH, STRING_SESSIONS

clients = []

# channel_id -> client
CHANNEL_CLIENTS = {}
CHANNELS = {}

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
    CHANNELS.clear()

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
            CHANNELS[entity.id] = entity

    return channels

async def get_channel_info(channel_id):

    client = CHANNEL_CLIENTS.get(channel_id)

    if client is None:
        return None

    entity = await client.get_entity(channel_id)

    full = await client(GetFullChannelRequest(entity))

    subscribers = full.full_chat.participants_count

    last_views = 0

    async for msg in client.iter_messages(entity, limit=1):
        last_views = msg.views or 0

    return {
        "client": client,
        "entity": entity,
        "title": entity.title,
        "subscribers": subscribers,
        "views": last_views
    }

async def get_channel(channel_id):

    client = CHANNEL_CLIENTS.get(channel_id)

    entity = CHANNELS.get(channel_id)

    if client is None or entity is None:
        return None

    return client, entity

async def rename_channel(channel_id: int, new_name: str):

    client = CHANNEL_CLIENTS.get(channel_id)

    entity = CHANNELS.get(channel_id)

    if client is None or entity is None:
        return False

    try:
        await client(
            EditTitleRequest(
                channel=entity,
                title=new_name
            )
        )

        entity.title = new_name

        return True

    except Exception as e:
        print(e)
        return False
