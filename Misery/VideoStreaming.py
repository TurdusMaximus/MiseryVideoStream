import re
from os import path
from asyncio import sleep
from youtube_dl import YoutubeDL
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import GroupCallFactory
from config import API_ID, API_HASH, SESSION_NAME, BOT_USERNAME
from helpers.decorators import authorized_users_only
from helpers.filters import command


STREAM = {8}
VIDEO_CALL = {}

ydl_opts = {
        "geo-bypass": True,
        "nocheckcertificate": True,
}
ydl = YoutubeDL(ydl_opts)


app = Client(
    SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
)
group_call_factory = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)


@Client.on_message(command(["vplay", f"vplay@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def vstream(_, m: Message):
    if 1 in STREAM:
        await m.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴠɪᴅᴇᴏ ᴏʀ ɢɪᴠᴇ ᴍᴇ ʏᴛ ʟɪɴᴋ ᴛᴏ sᴛʀᴇᴀᴍ!  ")
        return   

    media = m.reply_to_message
    if not media and not ' ' in m.text:
        await m.reply_text("** ɢɪᴠᴇ ᴍᴇ ᴀ ᴠɪᴅᴇᴏ ᴏʀ ᴜʀʟ ᴛᴏ sᴛʀᴇᴀᴍ ɪɴ ᴠᴄ!\n\n •ᴜsᴇ /vplay ᴄᴏᴍᴍᴀɴᴅ ʙʏ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴀ ᴠɪᴅᴇᴏ \n\nᴏʀ ɢɪᴠɪɴɢ ᴀɴ ᴜʀʟ ᴛᴏ sᴛʀᴇᴀᴍ ɪɴ ᴠᴄ**")

    elif ' ' in m.text:
        msg = await m.reply_text("🔄 **ᴘʀᴏᴄᴇssɪɴɢ..**")
        text = m.text.split(' ', 1)
        query = text[1]
        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex,query)
        if match:
            await msg.edit("🍺**ʏᴛ sᴛʀᴇᴀᴍɪɴɢ ɪs sᴛᴀʀᴛɪɴɢ ʙʏ ᴍɪsᴇʀʏ. ʙᴇ ʀᴇᴀᴅʏ ғᴏʀ ᴘᴀʀᴛʏ!**")
            try:
                meta = ydl.extract_info(query, download=False)
                formats = meta.get('formats', [meta])
                for f in formats:
                        ytstreamlink = f['url']
                ytstream = ytstreamlink
            except Exception as e:
                await msg.edit(f"❌ **ʏᴛ ᴇʀʀᴏʀ. ʀᴇᴘᴏʀᴛ ᴀᴛ sᴜᴘᴘᴏʀᴛ!** \n\n`{e}`")
                return
            await sleep(2)
            try:
                chat_id = m.chat.id
                group_call = group_call_factory.get_group_call()
                await group_call.join(chat_id)
                await group_call.start_video(ytstream, repeat=False)
                VIDEO_CALL[chat_id] = group_call
                await msg.edit((f"🍓 **•sᴛᴀʀᴛᴇᴅ [ʏᴛ sᴛʀᴇᴀᴍ ʙʏ ᴍɪsᴇʀʏ]({ytstream}) !\n\n•ᴊᴏɪɴ ᴠᴄ ᴀɴᴅ ᴇɴᴊᴏʏ.**"), disable_web_page_preview=True)
                await group_call.start_video(ytlink, repeat=False, enable_experimental_lip_sync=True)

       
                try:
                    STREAM.remove(0)
                except:
                    pass
                try:
                    STREAM.add(1)
                except:
                    pass
            except Exception as e:
                await msg.edit(f"❌ **sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ!** \n\n•Eʀʀᴏʀ: `{e}`")
        else:
            await msg.edit("•**ʟɪᴠᴇ sᴛʀᴇᴀᴍɪɴɢ ɪs sᴛᴀʀᴛɪɴɢ...**")
            livestream = query
            chat_id = m.chat.id
            await sleep(2)
            try:
                group_call = group_call_factory.get_group_call()
                await group_call.join(chat_id)
                await group_call.start_video(livestream, repeat=False)
                VIDEO_CALL[chat_id] = group_call
                await msg.edit((f"🍺 **sᴛᴀʀᴛᴇᴅ [ʟɪᴠᴇ sᴛʀᴇᴀᴍɪᴍɢ]({livestream}) !\n\n•ᴊᴏɪɴ ᴠᴄ ᴀɴᴅ ᴇɴᴊᴏʏ sᴛʀᴇᴀᴍɪɴɢ.**"), disable_web_page_preview=True)
                try:
                    STREAM.remove(0)
                except:
                    pass
                try:
                    STREAM.add(1)
                except:
                    pass
            except Exception as e:
                await msg.edit(f"❌ **sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ!** \n\n•ᴇʀʀᴏʀ: `{e}`")

    elif media.video or media.document:
        msg = await m.reply_text("📥 **Dᴏᴡɴʟᴏᴀᴅɪɴɢ..**")
        video = await media.download()
        chat_id = m.chat.id
        await sleep(2)
        try:
            group_call = group_call_factory.get_group_call()
            await group_call.join(chat_id)
            await group_call.start_video(video, repeat=False)
            VIDEO_CALL[chat_id] = group_call
            await msg.edit("🍓Vɪᴅᴇᴏ sᴛʀᴇᴀᴍɪɴɢ sᴛᴀʀᴛᴇᴅ!\n\n• ᴊᴏɪɴ ᴠᴄ ᴛᴏ ᴡᴀᴛᴄʜ ᴛʜᴇ ᴠɪᴅᴇᴏ!")
            try:
                STREAM.remove(0)
            except:
                pass
            try:
                STREAM.add(1)
            except:
                pass
        except Exception as e:
            await msg.edit(f"❌ sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ! \n\n•ᴇʀʀᴏʀ: `{e}`")
    else:
        await msg.edit("**ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴠɪᴅᴇᴏ ᴏʀ ᴜsᴇ ʏᴛ ᴜʀʟ ᴛᴏ sᴛʀᴇᴀᴍ ɪᴛ ɪɴ ᴠᴄ!**")
        return


@Client.on_message(command(["stop", f"stop@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def stop(_, m: Message):
    chat_id = m.chat.id
    if 0 in STREAM:
        await m.reply_text("ɢɪᴠᴇ ᴍᴇ ᴛʜᴇ ᴠɪᴅᴇᴏ ᴏʀ ʏᴛ ᴜʀʟ ᴛᴏ sᴛʀᴇᴀᴍ!\n\n •ᴜsᴇ ᴛʜᴇ /vplay ᴄᴏᴍᴍᴀɴᴅ ʙʏ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴀ ᴠɪᴅᴇᴏ\n\nᴏʀ ʙʏ ɢɪᴠɪɴɢ ʏᴛ ᴏʀ ʟɪᴠᴇ sᴛʀᴇᴀᴍ ᴜʀʟ")
        return
    try:
        await VIDEO_CALL[chat_id].stop()
        await m.reply_text("sᴛʀᴇᴀᴍɪɴɢ ᴇɴᴅᴇᴅ!")
                               
        try:
            STREAM.remove(1)
        except:
            pass
        try:
            STREAM.add(0)
        except:
            pass
    except Exception as e:
        await m.reply_text(f"❌ sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ! \n\n•ᴇʀʀᴏʀ: `{e}`")
        # Edited By TurdusMaximus
