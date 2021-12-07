from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from pyrogram.raw import functions
from pyrogram.raw.types import InputPeerUser
from .utils.utils import modules_help, prefix
from .utils.db import db


async def anti_pm_handler(client: Client, message: Message):
    status = db.get("core.antipm", "status", False)
    if (
        status
        and message.chat.type in ["private"]
        and (
            not message.from_user.is_contact
            and not message.from_user.is_bot
            and not message.from_user.is_self
        )
    ):
        await client.read_history(message.chat.id)
        user_info = await client.resolve_peer(message.chat.id)
        await message.delete()
        if db.get("core.antipm", "spamrep", False):
            await client.send(functions.messages.ReportSpam(peer=user_info))
        await client.send(
            functions.messages.DeleteHistory(
                peer=user_info, max_id=0, revoke=True
            )
        )


@Client.on_message(filters.command(["anti_pm"], prefix) & filters.me)
async def anti_pm(client: Client, message: Message):
    status = db.get("core.antipm", "status", False)
    if status:
        await message.edit("Анти-пм включен")
        my_handler = MessageHandler(anti_pm_handler, filters.private)
        client.add_handler(my_handler)
    else:
        db.set("core.antipm", "status", True)
        my_handler = MessageHandler(anti_pm_handler, filters.private)
        client.add_handler(my_handler)
        await message.edit("Анти-пм включен")


@Client.on_message(filters.command(["disable_anti_pm"], prefix) & filters.me)
async def disable_anti_pm(client: Client, message: Message):
    db.set("core.antipm", "status", False)
    await message.edit("Анти-пм выключен")


@Client.on_message(filters.command(["esr"], prefix) & filters.me)
async def esr(client: Client, message: Message):
    db.set("core.antipm", "spamrep", True)
    await message.edit("Спам репортами включен")


@Client.on_message(filters.command(["dsr"], prefix) & filters.me)
async def dsr(client: Client, message: Message):
    db.set("core.antipm", "spamrep", False)
    await message.edit("Спам репортами выключен")


modules_help.append(
    {
        "antipm": [
            {
                "anti_pm": "Удалить все сообщения от юзеров которых нет в контактах"
            },
            {"disable_anti_pm": "Выключить"},
            {"esr": "Включить спам репорт"},
            {"dsr": "Выключить спам репорт"},
        ]
    }
)
