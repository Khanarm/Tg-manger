from aiogram.utils.keyboard import InlineKeyboardBuilder


def panel_channels_keyboard(channels):
    builder = InlineKeyboardBuilder()

    for channel in channels:
        builder.button(
            text=f"📢 {channel.title}",
            callback_data=f"panel_channel_{channel.id}"
        )

    builder.adjust(1)

    return builder.as_markup()


def channel_info_keyboard(channel_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="⚙️ Edit",
        callback_data=f"panel_edit_{channel_id}"
    )

    builder.button(
        text="🔄 Refresh",
        callback_data=f"panel_channel_{channel_id}"
    )

    builder.button(
        text="⬅️ Back",
        callback_data="panel_back_channels"
    )

    builder.button(
        text="❌ Close",
        callback_data="panel_close"
    )

    builder.adjust(2)

    return builder.as_markup()


def edit_menu_keyboard(channel_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📝 Change Name",
        callback_data=f"panel_name_{channel_id}"
    )

    builder.button(
        text="👤 Change Username",
        callback_data=f"panel_username_{channel_id}"
    )

    builder.button(
    text="🖼 Change Photo",
    callback_data=f"setphoto_{channel_id}"
    )

    builder.button(
        text="📄 Change Bio",
        callback_data=f"panel_bio_{channel_id}"
    )

    builder.button(
        text="📢 Broadcast",
        callback_data=f"panel_broadcast_{channel_id}"
    )

    builder.button(
        text="📊 Statistics",
        callback_data=f"panel_stats_{channel_id}"
    )

    builder.button(
        text="⬅️ Channel Info",
        callback_data=f"panel_channel_{channel_id}"
    )

    builder.button(
        text="📋 Channel List",
        callback_data="panel_back_channels"
    )

    builder.button(
        text="❌ Close",
        callback_data="panel_close"
    )

    builder.adjust(2)

    return builder.as_markup()
