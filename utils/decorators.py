from functools import wraps

from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import settings

from services.user_service import UserService


def check_subscription(func):
    @wraps(func)
    async def wrapper(client: Client, message: Message, *args, **kwargs):
        user_service = UserService()
        user_data = {
            'user_id': message.from_user.id,
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name
        }
        user, created = user_service.get_or_create_user(user_data)

        if not user.is_active:
            await message.reply_text("You are banned from using this bot.")
            return

        if created:
            await client.send_message(
                settings.GROUP_ID,
                f"User using bot:\n"
                f"Name: {message.from_user.first_name}\n"
                f"Username: @{message.from_user.username}\n"
                f"ID: {message.from_user.id}\n"
            )

        try:
            user = await client.get_chat_member(settings.CHANNEL_ID, message.from_user.id)
            if user.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return await func(client, message, *args, **kwargs)
            else:
                await message.reply(
                    f"Please subscribe to our channel to use the bot",
                    reply_markup=await get_subscription_keyboard(),
                    quote=True
                )
        except Exception:
            await message.reply(
                f"Please subscribe to our channel to use the bot",
                reply_markup=await get_subscription_keyboard(),
                quote=True
            )

    return wrapper

async def get_subscription_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Join the channel", url=settings.CHANNEL_JOIN_LINK)],
        [InlineKeyboardButton(text="✅ Check subscription", callback_data="check_subscription")]
    ])
    return keyboard
