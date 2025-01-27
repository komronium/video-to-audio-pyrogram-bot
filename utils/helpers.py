import os
from typing import Optional, Callable
from pyrogram.types import Message
from moviepy import VideoFileClip


async def progress(current, total, message: Message, action: str):
    percent = (current / total) * 100
    bar_length = 20
    block = int(round(bar_length * current / total))
    filled_bar = "█" * block
    empty_bar = "░" * (bar_length - block)
    await message.edit_text(f"{action}: {percent:.2f}%\n{filled_bar}{empty_bar}")


async def convert_video_to_audio(video_path: str) -> Optional[str]:
    try:
        video = VideoFileClip(video_path)
        audio_path = video_path.rsplit(".", 1)[0] + ".mp3"
        video.audio.write_audiofile(audio_path)
        video.close()
        return audio_path
    except Exception as e:
        print(f"Error converting video to audio: {e}")
        return None


def clean_temp_files(*files):
    for file in files:
        try:
            if os.path.exists(file):
                os.remove(file)
        except Exception as e:
            print(f"Error removing file {file}: {e}")
