from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import CallbackQuery
from pyrogram.enums import ChatMemberStatus
from config import settings


@Client.on_callback_query(filters.regex('^check_subscription$'))
async def check_subscription(client: Client, callback: CallbackQuery):
    try:
        user = await client.get_chat_member(settings.CHANNEL, callback.from_user.id)
        if user.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            await callback.answer('❌ You haven\'t subscribed to the channel yet!', show_alert=True)
            return
    except UserNotParticipant:
        await callback.answer('❌ You haven\'t subscribed to the channel yet!', show_alert=True)
        return

    await callback.message.delete()
    await callback.message.reply("✅ Thank you! You can now use the bot")
