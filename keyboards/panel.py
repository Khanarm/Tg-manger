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
        text="⬅️ Back",
        callback_data="panel_back_channels"
    )

    builder.adjust(2)

    return builder.as_markup()


def edit_menu_keyboard(channel_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📝 Change Name",
        callback_data=f"edit_name_{channel_id}"
    )

    builder.button(
        text="👤 Change Username",
        callback_data=f"edit_username_{channel_id}"
    )

    builder.button(
        text="🖼 Change Photo",
        callback_data=f"edit_photo_{channel_id}"
    )

    builder.button(
        text="📄 Change Bio",
        callback_data=f"edit_bio_{channel_id}"
    )

    builder.button(
        text="📢 Broadcast",
        callback_data=f"edit_broadcast_{channel_id}"
    )

    builder.button(
        text="🔄 Refresh Info",
        callback_data=f"panel_channel_{channel_id}"
    )

    builder.button(
        text="⬅️ Back",
        callback_data=f"panel_channel_{channel_id}"
    )

    builder.adjust(1)

    return builder.as_markup()
