from pyrogram import Client, filters
from .utils.utils import modules_help, prefix
from pyrogram.handlers import MessageHandler
import datetime
import asyncio


async def afk_handler(client, message):
    try:
        global start, end
        end = datetime.datetime.now().replace(microsecond=0)
        afk_time = end - start
        if message.from_user.is_bot is False:
            await message.reply_text(
                f"<b>Я ушёл в афк {afk_time}</b>\n" f"<b>Причина:</b> <i>{reason}</i>"
            )
    except NameError:
        pass


@Client.on_message(filters.command("afk", prefix) & filters.me)
async def afk(client, message):
    global start, end, handler, reason
    start = datetime.datetime.now().replace(microsecond=0)
    handler = client.add_handler(
        MessageHandler(afk_handler, (filters.private & ~filters.me))
    )
    if len(message.text.split()) >= 2:
        reason = message.text.split(" ", maxsplit=1)[1]
    else:
        reason = "None"
    await message.edit("<b>Я ухожу в афк</b>")


@Client.on_message(filters.command("unafk", prefix) & filters.me)
async def unafk(client, message):
    try:
        global start, end
        end = datetime.datetime.now().replace(microsecond=0)
        afk_time = end - start
        await message.edit(f"<b>Я вышел из афк.\nЯ был афк на протяжении {afk_time}</b>")
        client.remove_handler(*handler)
    except NameError:
        await message.edit("<b>Ты не афк</b>")
        await asyncio.sleep(3)
        await message.delete()


modules_help.append(
    {"afk": [{"afk [reason]": "АФК"}, {"unafk": "Из афк"}]}
)
