import asyncio
from datetime import datetime

from database.scheduled import (
    get_pending_tasks,
    mark_completed,
    mark_failed,
)

from userbot.client import (
    rename_channel,
    update_channel_username_auto,
    update_channel_photo_from_link,
    send_channel_post_from_link,
)


async def execute_task(task):

    task_id = str(task["_id"])

    try:

        channel_id = task["channel_id"]
        data = task["data"]
        action = data["action"]

        if action == "rename":

            success = await rename_channel(
                channel_id,
                data["name"]
            )
            result = "Success"

        elif action == "username":

            success, result = await update_channel_username_auto(
                channel_id,
                data["username"]
            )

        elif action == "photo":

            success, result = await update_channel_photo_from_link(
                channel_id,
                data["photo_link"]
            )

        elif action == "post":

            success, result = await send_channel_post_from_link(
                channel_id,
                data["post_link"]
            )

        elif action == "update_channel":

            success = await rename_channel(
                channel_id,
                data["name"]
            )
            result = "Success"

            if success and data.get("username"):
                success, result = await update_channel_username_auto(
                    channel_id,
                    data["username"]
                )

            if success and data.get("photo_link"):
                success, result = await update_channel_photo_from_link(
                    channel_id,
                    data["photo_link"]
                )

            if success and data.get("post_link"):
                success, result = await send_channel_post_from_link(
                    channel_id,
                    data["post_link"]
                )

        else:

            raise Exception(f"Unknown action: {action}")

        if success:

            await mark_completed(task_id)
            print(f"✅ Task completed {task_id}")

        else:

            await mark_failed(task_id, result)

    except Exception as e:

        print("Task Error:", e)

        await mark_failed(task_id, str(e))


async def task_scheduler():

    print("⏰ Task Scheduler Started")

    while True:

        try:

            tasks = await get_pending_tasks()

            now = datetime.utcnow()

            print("PENDING TASK COUNT:", len(tasks))
            print("CURRENT TIME:", now)

            for task in tasks:

                print("TASK TIME:", task["run_at"])

                if task["run_at"] <= now:

                    await execute_task(task)

        except Exception as e:

            print("Scheduler Error:", e)

        await asyncio.sleep(30)
