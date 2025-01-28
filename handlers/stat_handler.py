from pyrogram import Client, filters
from pyrogram.types import Message

from services.user_service import UserService
from utils.decorators import check_subscription


@Client.on_message(filters.command('stats'))
@check_subscription
async def stat_command(client: Client, message: Message):
    user_service = UserService()
    user_count = user_service.get_user_count()
    today_joined_user_count = user_service.get_today_joined_user_count()
    conversion_count = user_service.get_conversion_count()
    active_user_count = user_service.get_active_user_count()

    response_message = (
        "<b>BOT STATISTICS</b>\n\n"
        f"Total Users:  <b>{user_count}</b>\n"
        f"Active Users:  <b>{active_user_count}</b>\n"
        f"Users Joined Today:  <b>{today_joined_user_count}</b>\n"
        f"Total Conversions:  <b>{conversion_count}</b>\n"
    )

    await client.send_message(message.chat.id, response_message)
