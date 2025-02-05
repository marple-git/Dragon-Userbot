from time import perf_counter
from pyrogram import Client, filters
from pyrogram.methods import messages
from pyrogram.types import Message
from html import escape as t
from pyrogram.errors.exceptions.flood_420 import FloodWait
from .utils.utils import modules_help, prefix
from .utils.db import db
from pyrogram.raw.functions.messages.get_all_chats import GetAllChats
import json


@Client.on_message(filters.command("admlist", prefix) & filters.me)
async def ownlist(client: Client, message: Message):
    tstart = perf_counter()
    await message.edit("<code>Получаю информацию...</code>")
    chatlist = []
    try:
        _ = await client.send(GetAllChats(except_ids=[]))
        chats = json.loads(str(_))
        for chat in chats["chats"]:
            if chat.get("migrated_to") is None and (
                chat.get("creator") is True
                or chat.get("admin_rights") is not None
            ):
                role = "creator" if chat.get("creator") is True else "administrator"
                chatlist.append(
                    {
                        "chat_name": str(chat["title"]),
                        "chat_id": chat["id"],
                        "role": role,
                        "username": chat.get("username"),
                        "link": "https://t.me/c/{}/1".format(chat["id"]),
                    }
                )

        adminned_chats = "<b>Админ в чатах:</b>\n"
        owned_chats = "<b>Владелец чатов:</b>\n"
        owned_chats_with_username = "<b>Владелец чатов с юзернеймом:</b>\n"

        c_adminned_chats = 0
        c_owned_chats = 0
        c_owned_chats_with_username = 0

        for chat in chatlist:
            if chat["role"] == "creator" and chat["username"] is not None:
                c_owned_chats_with_username += 1
                owned_chats_with_username += f'{c_owned_chats_with_username}. <a href="{chat["link"]}">{t(chat["chat_name"])}</a> - @{chat["username"]}\n'
            elif chat["role"] == "creator":
                c_owned_chats += 1
                owned_chats += f'{c_owned_chats}. <a href="{chat["link"]}">{t(chat["chat_name"])}</a>\n'
            elif chat["role"] == "administrator":
                c_adminned_chats += 1
                adminned_chats += f'{c_adminned_chats}. <a href="{chat["link"]}">{t(chat["chat_name"])}</a>\n'
        stats = f"<b><u>Всего:</u></b> {len(chatlist)}\n<b><u>Админ в чатах:</u></b> {c_adminned_chats}\n<b><u>Владелец в чатах:</u></b> {c_owned_chats}\n<b><u>Владелец в чатах с юзернеймом:</u></b> {c_owned_chats_with_username}"
        tstop = perf_counter()
        await message.edit(
            adminned_chats
            + "\n"
            + owned_chats
            + "\n"
            + owned_chats_with_username
            + "\n"
            + stats
            + "\n\n"
            + f"Done at {int(tstop - tstart)} seconds.",
            disable_web_page_preview=True,
        )
    except FloodWait as e:
        await message.edit(
            "<b>Error occured.</b>\n<code>FloodWait. Try again in {} seconds</code>".format(
                e.x
            )
        )


modules_help.append({"admlist": [{"admlist": "Получить чаты где ты админ"}]})
