from telethon import events
from telethon.tl.functions.messages import ForwardMessagesRequest
from config import OWNER_ID
from database.mongo import get_all_channels


def register(bot):

    @bot.on(events.NewMessage(pattern="/broadcast"))
    async def broadcast(event):

        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized.")
            return

        await event.reply(
            "📢 Broadcast Mode\n\n"
            "Ab jo message bhejoge, woh sabhi channels me forward hoga."
        )

        @bot.on(events.NewMessage(from_users=OWNER_ID))
        async def send_broadcast(msg):

            if msg.raw_text == "/broadcast":
                return

            channels = await get_all_channels()

            if not channels:
                await msg.reply("❌ No channels added.")
                return

            success = 0

            for channel in channels:
                try:
                    await bot.forward_messages(
                        entity=channel["channel_id"],
                        messages=msg.message
                    )
                    success += 1
                except Exception as e:
                    print(e)

            await msg.reply(f"✅ Broadcast sent to {success} channel(s).")

            bot.remove_event_handler(send_broadcast)
