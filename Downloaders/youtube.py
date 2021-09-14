from os import path

from youtube_dl import YoutubeDL

from config import DURATION_LIMIT
from helpers.errors import DurationLimitError

ydl_opts = {
    "format": "bestaudio/best",
    "verbose": True,
    "addmetadata": True,
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}

ydl = YoutubeDL(ydl_opts)


def download(url: str) -> str:
    global ydl
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 60)

    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"🛑 ᴍɪsᴇʀʏ ᴄᴀɴɴᴏᴛ ᴘʟᴀʏ ᴠɪᴅᴇᴏs ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs. ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ᴠɪᴅᴇᴏ ɪs {duration} ᴍɪɴᴜᴛᴇs"
        )
    try:
        ydl.download([url])
    except:
        raise DurationLimitError(
            f"🛑 ᴍɪsᴇʀʏ ᴄᴀɴɴᴏᴛ ᴘʟᴀʏ ᴠɪᴅᴇᴏs ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs. ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ᴠɪᴅᴇᴏ ɪs {duration} ᴍɪɴᴜᴛᴇs"
        )
    return path.join("downloads", f"{info['id']}.{info['ext']}")
