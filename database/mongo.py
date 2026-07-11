from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

from config import (
    MONGO_URI,
    DATABASE_NAME,
)

client = AsyncIOMotorClient(MONGO_URI)

db = client[DATABASE_NAME]

channels = db.channels
settings = db.settings
broadcast_logs = db.broadcast_logs


async def save_channel(
    channel_id: int,
    title: str,
    username: str = None,
):
    await channels.update_one(
        {
            "channel_id": channel_id
        },
        {
            "$set": {
                "title": title,
                "username": username,
                "updated_at": datetime.utcnow()
            }
        },
        upsert=True
    )


async def get_channel(channel_id: int):
    return await channels.find_one(
        {
            "channel_id": channel_id
        }
    )


async def get_all_channels():
    result = []

    async for channel in channels.find():
        result.append(channel)

    return result
