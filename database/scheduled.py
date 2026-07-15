from datetime import datetime

from .mongo import db

from bson import ObjectId


scheduled_tasks = db.scheduled_tasks


async def create_task(channel_id, data, run_at):

    print("CREATE_TASK START")

    result = await scheduled_tasks.insert_one({
        "channel_id": channel_id,
        "data": data,
        "run_at": run_at,
        "status": "pending",
        "created_at": datetime.utcnow(),
        "completed_at": None,
        "error": None,
        "log_message_id": None,
    })

    print("INSERTED ID:", result.inserted_id)

    return str(result.inserted_id)



async def get_pending_tasks():

    tasks = []

    now = datetime.utcnow()

    async for task in scheduled_tasks.find(
        {
            "status": "pending",
            "run_at": {
                "$lte": now
            }
        }
    ):
        tasks.append(task)

    return tasks




async def mark_completed(task_id):

    await scheduled_tasks.update_one(
        {
            "_id": ObjectId(task_id)
        },
        {
            "$set": {
                "status": "completed",
                "completed_at": datetime.utcnow()
            }
        }
    )



async def mark_failed(
    task_id,
    error
):

    await scheduled_tasks.update_one(
        {
            "_id": ObjectId(task_id)
        },
        {
            "$set": {
                "status": "failed",
                "error": str(error)
            }
        }
    )



async def get_channel_tasks(
    channel_id
):

    tasks = []

    async for task in scheduled_tasks.find(
        {
            "channel_id": channel_id
        }
    ).sort(
        "run_at",
        1
    ):
        tasks.append(task)

    return tasks



async def delete_task(
    task_id
):

    await scheduled_tasks.delete_one(
        {
            "_id": ObjectId(task_id)
        }
    )

async def update_log_message_id(
    task_id,
    message_id
):

    await scheduled_tasks.update_one(
        {
            "_id": ObjectId(task_id)
        },
        {
            "$set": {
                "log_message_id": message_id
            }
        }
    )
