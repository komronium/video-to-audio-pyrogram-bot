from pyrogram import Client, filters
from pyrogram.types import Message

from services.user_service import UserService
from utils.decorators import check_subscription
from utils.helpers import convert_video_to_audio, clean_temp_files, progress
from config import settings


@Client.on_message(filters.video)
@check_subscription
async def video_handler(client: Client, message: Message):
    try:
        video = message.video
        if video.file_size > 100 * 1024 * 1024:
            await message.reply('Sorry, but we can only process files up to 100 MB in size')
            return

        progress_msg = await message.reply_text("Downloading video...", quote=True)
        video_path = await message.download(
            progress=progress,
            progress_args=(progress_msg, 'Downloading')
        )

        await progress_msg.edit_text("Converting to audio...")

        async def conversion_progress(current, total):
            await progress(current, total, progress_msg, "Converting")

        audio_path = await convert_video_to_audio(video_path)

        if not audio_path:
            await progress_msg.edit_text("Error converting video to audio!")
            return

        # Send audio
        user_service = UserService()
        user_service.update_activity(message.from_user.id)
        await progress_msg.edit_text("Sending audio...")
        bot = await client.get_me()
        await message.reply_audio(
            audio_path,
            caption=f"Converted by @{bot.username}",
            quote=True
        )
        await progress_msg.delete()

    except Exception as e:
        await message.reply_text(f"Error: {str(e)}", quote=True)
    finally:
        # Clean up temporary files
        clean_temp_files(video_path, audio_path)
