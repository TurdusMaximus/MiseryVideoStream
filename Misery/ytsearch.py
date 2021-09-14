import logging
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from pyrogram import Client as app
from helpers.filters import command
from config import BOT_USERNAME


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


@app.on_message(command(["search", f"search@{BOT_USERNAME}"]))
async def ytsearch(_, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text("/Search ɴᴇᴇᴅs ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴏᴘᴇʀᴀᴛᴇ!")
            return
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("🔎 **sᴇᴀʀᴄʜɪɴɢ..**")
        results = YoutubeSearch(query, max_results=5).to_dict()
        i = 0
        text = ""
        while i < 5:
            text += f"**•Nᴀᴍᴇ:** `{results[i]['title']}`\n"
            text += f"**•Dᴜʀᴀᴛɪᴏɴ:** {results[i]['duration']}\n"
            text += f"**•Vɪᴇᴡs:** {results[i]['views']}\n"
            text += f"**•Cʜᴀɴɴᴇʟ:** {results[i]['channel']}\n"
            text += f"https://www.youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await m.edit(text, disable_web_page_preview=True)
    except Exception as e:
        await m.edit(str(e))
