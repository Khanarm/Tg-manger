from telethon import events, Button

from userbot.channel import get_channel_info


def register(bot):

    @bot.on(events.CallbackQuery)
    async def callback_handler(event):

        data = event.data.decode()

        if ":" not in data:
            return

        action, channel_id = data.split(":")

        info = await get_channel_info(int(channel_id))

        if not info:
            await event.answer(
                "Channel not found.",
                alert=True
            )
            return

        text = (
            f"📢 {info['title']}\n\n"
            f"👥 Subscribers : {info['subscribers']}\n"
            f"👁 Last Post Views : {info['views']}\n\n"
            f"⚙ Action : {action}"
        )

        buttons = [
            [
                Button.inline(
                    "⬅ Back",
                    data=f"back:{action}".encode()
                ),
                Button.inline(
                    "✅ Confirm",
                    data=f"confirm:{action}:{channel_id}".encode()
                )
            ]
        ]

        await event.edit(
            text,
            buttons=buttons
        )
