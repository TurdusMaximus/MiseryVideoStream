from pyrogram import Client, errors
from pyrogram.types import (
    InlineQuery,
    InlineQueryResult,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from youtubesearchpython import VideosSearch


@Client.on_inline_query()
async def inline(client: Client, query: InlineQuery):
    answers = []
    search_query = query.query.lower().strip().rstrip()

    if search_query == "menu":
        await client.answer_inline_query(
            query.id,
            results=menus,
            switch_pm_text="Menu",
            switch_pm_parameter="help",
            cache_time=0,
        )
    if search_query == "":
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text="sᴇᴀʀᴄʜ ᴀ ʏᴛ ᴠɪᴅᴇᴏ ғʀᴏᴍ ʜᴇʀᴇ",
            switch_pm_parameter="help",
            cache_time=0,
        )
    else:
        search = VideosSearch(search_query, limit=50)

        for result in search.result()["result"]:
            answers.append(
                InlineQueryResultArticle(
                    title=result["•ᴛɪᴛʟᴇ -"],
                    description="{}, {} ᴠɪᴇᴡs.".format(
                        result["•ᴅᴜʀᴀᴛɪᴏɴ - "], result["viewCount"]["short"]
                    ),
                    input_message_content=InputTextMessageContent(
                        "/vplay https://www.youtube.com/watch?v={}".format(result["id"])
                    ),
                    thumb_url=result["thumbnails"][0]["url"],
                )
            )

        try:
            await query.answer(results=answers, cache_time=0)
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text="ᴇʀʀᴏʀ: sᴇᴀʀᴄʜ ᴛɪᴍᴇ ᴏᴜᴛ!",
                switch_pm_parameter="",
            )
# ==================
# Tested

menus = [
        InlineQueryResultArticle(title="sᴛᴀʀᴛ", description="sᴛᴀʀᴛ ʙᴏᴛ", input_message_content=InputTextMessageContent("/start")),
        InlineQueryResultArticle(title="ɪɴғᴏ", description="ɢᴇᴛ ɪɴғᴏ ᴀʙᴏᴜᴛ ʙᴏᴛ", input_message_content=InputTextMessageContent("/help")),
    ]
