from telethon import TelegramClient
from telethon.sessions import StringSession

from telethon.tl.types import (
    Channel,
    InputChatUploadedPhoto,
)

from telethon.tl.functions.channels import (
    GetFullChannelRequest,
    EditTitleRequest,
    UpdateUsernameRequest,
    EditPhotoRequest,
)

from config import API_ID, API_HASH, STRING_SESSIONS

clients = []

# channel_id -> client
CHANNEL_CLIENTS = {}
CHANNELS = {}


async def start_userbots():
    clients.clear()

    for session in STRING_SESSIONS:

        client = TelegramClient(
            StringSession(session),
            API_ID,
            API_HASH,
        )

        await client.start()

        me = await client.get_me()
        print(f"✅ Started: {me.first_name}")

        count = 0

        async for dialog in client.iter_dialogs():
            if dialog.is_channel:
                print(f"📢 {dialog.name}")
                count += 1

        print(f"✅ Total Channels = {count}")

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

    entity = CHANNELS.get(channel_id)

    if entity is None:
        entity = await client.get_entity(channel_id)

    full = await client(GetFullChannelRequest(entity))

    subscribers = getattr(
        full.full_chat,
        "participants_count",
        0,
    )

    views = 0

    async for msg in client.iter_messages(entity, limit=1):
        views = getattr(msg, "views", 0) or 0

    return {
        "client": client,
        "entity": entity,
        "title": entity.title,
        "username": entity.username,
        "subscribers": subscribers,
        "views": views,
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
                title=new_name,
            )
        )

        print("\n========== LAST 5 MESSAGES ==========")

        async for msg in client.iter_messages(entity, limit=5):
            print(f"ID: {msg.id}")
            print(f"TEXT: {msg.text}")
            print(f"ACTION: {msg.action}")
            print(f"TYPE: {type(msg)}")
            print("--------------------------------")

        entity.title = new_name

        return True

    except Exception as e:
        print("Rename Error:", e)
        return False


async def update_channel_username(channel_id: int, new_username: str):

    client = CHANNEL_CLIENTS.get(channel_id)
    entity = CHANNELS.get(channel_id)

    if client is None or entity is None:
        return False, "Channel not found"

    try:

        await client(
            UpdateUsernameRequest(
                channel=entity,
                username=new_username
            )
        )

        return True, "Username updated successfully"

    except Exception as e:
        print("Username Error:", e)
        return False, str(e)


async def update_channel_photo(channel_id: int, photo_path: str):

    client = CHANNEL_CLIENTS.get(channel_id)
    entity = CHANNELS.get(channel_id)

    if client is None or entity is None:
        return False, "Channel not found"

    try:

        uploaded = await client.upload_file(photo_path)

        await client(
            EditPhotoRequest(
                channel=entity,
                photo=InputChatUploadedPhoto(uploaded)
            )
        )

        return True, "Photo updated successfully"

    except Exception as e:
        print("Photo Error:", e)
        return False, str(e)
