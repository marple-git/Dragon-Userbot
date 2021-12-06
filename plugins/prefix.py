from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import config, config_path, modules_help, prefix
from .utils.scripts import restart
from .utils.db import db


@Client.on_message(
    filters.command(["sp", "setprefix", "setprefix_dragon"], prefix) & filters.me
)
async def pref(client: Client, message: Message):
    if len(message.command) > 1:
        prefix = message.command[1]
        print(message.command)
        db.set("core.main", "prefix", prefix)
        await message.edit(f"<b>Префикс [ <code>{prefix}</code> ] установлен!</b>")
        await restart()
    else:
        await message.edit("<b>Префикс не может быть пустым!</b>")


modules_help.append(
    {
        "prefix": [
            {"setprefix [prefix]*": "Установить кастомный префикс"},
            {"setprefix_dragon [prefix]*": "Установить кастомный префикс"},
        ]
    }
)
