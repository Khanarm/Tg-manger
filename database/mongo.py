from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)

db = client["tg_manager"]

# Collections
userbots = db["userbots"]
channels = db["channels"]


# ==========================
# USERBOT
# ==========================

async def save_userbot(user_id: int, session: str):
    await userbots.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "user_id": user_id,
                "session": session
            }
        },
        upsert=True
    )


async def get_userbot(user_id: int):
    return await userbots.find_one({"user_id": user_id})


async def get_all_userbots():
    data = []
    async for bot in userbots.find():
        data.append(bot)
    return data


# ==========================
# CHANNEL
# ==========================

async def save_channel(
    channel_id: int,
    title: str,
    username: str,
    userbot_id: int
):
    await channels.update_one(
        {"channel_id": channel_id},
        {
            "$set": {
                "channel_id": channel_id,
                "title": title,
                "username": username,
                "userbot_id": userbot_id
            }
        },
        upsert=True
    )


async def get_channel(channel_id: int):
    return await channels.find_one(
        {"channel_id": channel_id}
    )


async def get_all_channels():
    data = []
    async for ch in channels.find():
        data.append(ch)
    return data


async def delete_channel(channel_id: int):
    await channels.delete_one(
        {"channel_id": channel_id}
)
