import logging
from pyrogram import Client
from config import settings

app = Client(
    "VideoToAudioBot",
    api_id=settings.API_ID,
    api_hash=settings.API_HASH,
    bot_token=settings.BOT_TOKEN,
    plugins=dict(root='handlers')
)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run()
