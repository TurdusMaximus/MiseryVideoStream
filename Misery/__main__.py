from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
from Misery.VideoStreaming import app


Misery = Client(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Misery"),
)

Misery.start()
print("[Your Misery Is Ready To Stream✓")
app.start()
print("Started Sucksexfully✓")
idle()
