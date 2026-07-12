from datetime import datetime

from .mongo import db

scheduled_tasks = db.scheduled_tasks


async def create_task(
    channel_id: int,
    action: str,
    value: str,
    run_at: datetime,
):

    result = await scheduled_tasks.insert_one(
        {
            "channel_id": channel_id,
            "action": action,
            "value": value,
            "run_at": run_at,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "completed_at": None,
            "error": None,
        }
    )

    return str(result.inserted_id)


async def get_pending_tasks():

    result = []

    async for task in scheduled_tasks.find(
        {
            "status": "pending"
        }
    ):
        result.append(task)

    return result


async def mark_completed(task_id):

    from bson import ObjectId

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


async def mark_failed(task_id, error):

    from bson import ObjectId

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


async def get_channel_tasks(channel_id):

    result = []

    async for task in scheduled_tasks.find(
        {
            "channel_id": channel_id
        }
    ).sort(
        "run_at",
        1
    ):
        result.append(task)

    return result


async def delete_task(task_id):

    from bson import ObjectId

    await scheduled_tasks.delete_one(
        {
            "_id": ObjectId(task_id)
        }
          )
