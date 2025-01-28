from pyrogram import Client, filters
from pyrogram.types import Message

from services.user_service import UserService
from utils.decorators import check_subscription


@Client.on_message(filters.command("top"))
@check_subscription
async def stat_command(client: Client, message: Message):
    user_service = UserService()
    top_users = user_service.get_top_5_user()

    response_message = "<b>Top 5 Users</b>\n\n"

    for idx, user in enumerate(top_users, start=1):
        response_message += f"<b>{idx}</b>. {user.full_name[:20]} - <b>{user.conversion_count}</b>\n"

    await client.send_message(message.chat.id, response_message)
