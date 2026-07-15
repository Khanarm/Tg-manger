from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

from config import (
    MONGO_URI,
    DATABASE_NAME,
)

client = AsyncIOMotorClient(MONGO_URI)

db = client[DATABASE_NAME]

print("===================================")
print("DATABASE_NAME:", DATABASE_NAME)
print("DB NAME:", db.name)
print("===================================")

channels = db.channels
settings = db.settings
broadcast_logs = db.broadcast_logs
scheduled_tasks = db.scheduled_tasks

print("COLLECTION:", scheduled_tasks.name)

async def save_channel(
    channel_id: int,
    title: str,
    username: str = None,
    session_index: int = 0,
):
    await channels.update_one(
        {
            "channel_id": channel_id
        },
        {
            "$set": {
                "title": title,
                "username": username,
                "session_index": session_index,
                "updated_at": datetime.utcnow()
            },
            "$setOnInsert": {
                "last_original_post_id": None,
                "last_broadcast_id": None,
                "last_broadcast_at": None,
                "auto_broadcast": True
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
