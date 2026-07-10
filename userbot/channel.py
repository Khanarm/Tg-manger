from telethon.tl.types import Channel
from telethon import functions
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetHistoryRequest

from userbot.client import get_all_clients


async def get_all_channels():
    """
    Get all channels from all running userbots.
    """

    channels = []

    clients = get_all_clients()

    print("========== DEBUG ==========")
    print("Clients:", clients)

    for userbot_id, client in clients.items():

        try:
            me = await client.get_me()
            print(f"Logged in UserBot: {userbot_id}")
            print(f"User: {me.id} | {me.first_name}")

            dialogs = await client.get_dialogs()
            print(f"Dialogs Found: {len(dialogs)}")

            for dialog in dialogs:

                entity = dialog.entity

                print(
                    type(entity),
                    getattr(entity, "title", None),
                    getattr(entity, "broadcast", False),
                    getattr(entity, "creator", False)
                )

                if (
                    isinstance(entity, Channel)
                    and entity.broadcast
                    and entity.creator
                ):
                    print("FOUND CHANNEL:", entity.title)

                    channels.append({
                        "channel_id": entity.id,
                        "title": entity.title,
                        "username": entity.username,
                        "userbot_id": userbot_id,
                    })

        except Exception as e:
            print("ERROR:", e)

    print("TOTAL CHANNELS:", len(channels))
    print("===========================")

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

        except Exception:
            continue

    return None


async def set_channel_name(channel_id: int, new_name: str):

    info = await get_channel_info(channel_id)

    if not info:
        return False

    try:
        await info["client"](
            functions.channels.EditTitleRequest(
                channel=info["entity"],
                title=new_name
            )
        )
        return True

    except Exception as e:
        print(e)
        return False


async def set_channel_bio(channel_id: int, new_bio: str):

    info = await get_channel_info(channel_id)

    if not info:
        return False

    try:
        await info["client"](
            functions.channels.EditAboutRequest(
                channel=info["entity"],
                about=new_bio
            )
        )
        return True

    except Exception as e:
        print(e)
        return False


async def set_channel_username(channel_id: int, username: str):

    info = await get_channel_info(channel_id)

    if not info:
        return False

    try:
        await info["client"](
            functions.channels.UpdateUsernameRequest(
                channel=info["entity"],
                username=username
            )
        )
        return True

    except Exception as e:
        print(e)
        return False
