from telethon.tl.types import Channel
from userbot.client import get_all_clients

from telethon import functions
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetHistoryRequest

async def get_channels():
    """
    Get all channels from all running userbots.
    """

    channels = []

    clients = get_all_clients()

    for userbot_id, client in clients.items():

        dialogs = await client.get_dialogs()

        for dialog in dialogs:

            entity = dialog.entity

            if (
                isinstance(entity, Channel)
                and entity.broadcast
                and entity.creator
            ):

                channels.append({
                    "channel_id": entity.id,
                    "title": entity.title,
                    "username": entity.username,
                    "userbot_id": userbot_id,
                })

    return channels

async def get_channel_info(channel_id: int):

    clients = get_all_clients()

    for userbot_id, client in clients.items():

        try:
            entity = await client.get_entity(channel_id)

            full = await client(GetFullChannelRequest(entity))

            subscribers = full.full_chat.participants_count or 0

            history = await client(
                GetHistoryRequest(
                    peer=entity,
                    limit=1,
                    offset_date=None,
                    offset_id=0,
                    max_id=0,
                    min_id=0,
                    add_offset=0,
                    hash=0
                )
            )

            views = 0

            if history.messages:
                views = getattr(history.messages[0], "views", 0)

            return {
                "client": client,
                "userbot_id": userbot_id,
                "entity": entity,
                "title": entity.title,
                "subscribers": subscribers,
                "views": views
            }

        except:
            continue

    return None
