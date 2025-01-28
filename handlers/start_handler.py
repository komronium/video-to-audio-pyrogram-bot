from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.decorators import check_subscription
from config import settings


@Client.on_message(filters.command("start"))
@check_subscription
async def start_command(client: Client, message: Message):
    await message.reply_text(
        "Welcome to Video to Audio Bot! 🎵\n"
        "Send me any video and I'll convert it to audio.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Channel", url=f"https://t.me/{settings.CHANNEL}")]
        ])
    )
