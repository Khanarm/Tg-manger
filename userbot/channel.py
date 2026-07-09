from telethon.tl.types import Channel
from userbot.client import get_all_clients


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
