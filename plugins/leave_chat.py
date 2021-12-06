from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix
import asyncio


@Client.on_message(filters.command(["leave_chat", "lc"], prefix) & filters.me)
async def leave_chat(client: Client, message: Message):
    if message.chat.type in ["group", "supergroup"]:
        await message.edit("<code>Прощай...</code>")
        await asyncio.sleep(3)
        await client.leave_chat(chat_id=message.chat.id)
    else:
        await message.edit("Это не группа/супергруппа")


modules_help.append({"leave_chat": [{"leave_chat": "Выйти из чата"}]})
