import asyncio

from database.mongo import get_all_channels


async def broadcast_scheduler():

    while True:

        print("🔄 Broadcast Scheduler Running...")

        channels = await get_all_channels()

        for channel in channels:

            print(
                f"📢 Checking: {channel['title']}"
            )

        # 24 Hours
        await asyncio.sleep(86400)
