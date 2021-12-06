from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix
from pyrogram.raw import functions
from .utils.scripts import date_dict
import asyncio


@Client.on_message(filters.command("inf", prefix) & filters.me)
async def get_user_inf(client: Client, message: Message):
    if len(message.text.split()) >= 2:
        try:
            user = await client.get_users(message.text.split()[1])
            user = user.id
        except:
            try:
                user = message.reply_to_message.from_user.id
            except:
                user = message.from_user.id
    else:
        try:
            user = message.reply_to_message.from_user.id
        except:
            user = message.from_user.id
    user_info = await client.send(
        functions.users.GetFullUser(id=await client.resolve_peer(user))
    )
    if user_info.user.username == None:
        username = "None"
    else:
        username = f"@{user_info.user.username}"
    if user_info.about == None:
        about = "None"
    else:
        about = user_info.about
    user_info = f"""|=<b>Username: {username}
|-ID: <code>{user_info.user.id}</code>
|-Бот: <code>{user_info.user.bot}</code>
|-Скам: <code>{user_info.user.scam}</code>
|-Имя: <code>{user_info.user.first_name}</code>
|-Удалён: <code>{user_info.user.deleted}</code>
|-Био: <code>{about}</code>
</b>"""
    await message.edit(user_info)


@Client.on_message(filters.command("inffull", prefix) & filters.me)
async def get_full_user_inf(client: Client, message: Message):
    await message.edit("<code>Получаю информацию...</code>")
    if len(message.text.split()) >= 2:
        try:
            user = await client.get_users(message.text.split()[1])
            user = user.id
        except:
            try:
                user = message.reply_to_message.from_user.id
            except:
                user = message.from_user.id
    else:
        try:
            user = message.reply_to_message.from_user.id
        except:
            user = message.from_user.id
    try:
        await client.send_message("@creationdatebot", '/start')
        await asyncio.sleep(1)
        date_dict.clear()
        msg = await client.send_message("@creationdatebot", f"/id {user}")
        await asyncio.sleep(1)
        await client.send(
            functions.messages.DeleteHistory(
                peer=await client.resolve_peer(747653812), max_id=msg.chat.id
            )
        )
        user_info = await client.send(
            functions.users.GetFullUser(id=await client.resolve_peer(user))
        )
        if user_info.user.username is None:
            username = "None"
        else:
            username = f"@{user_info.user.username}"
        about = "None" if user_info.about is None else user_info.about
        user_info = f"""|=<b>Username: {username}
|-Id: <code>{user_info.user.id}</code>
|-Дата создания аккаунта: <code>{date_dict.get('date')}</code>
|-Бот: <code>{user_info.user.bot}</code>
|-Скам: <code>{user_info.user.scam}</code>
|-Имя: <code>{user_info.user.first_name}</code>
|-Удалён: <code>{user_info.user.deleted}</code>
|-Био: <code>{about}</code>
|-Контакт: <code>{user_info.user.contact}</code>
|-Может закреплять сообщения: <code>{user_info.can_pin_message}</code>
|-Взаимный контакт: <code>{user_info.user.mutual_contact}</code>
|-Access hash: <code>{user_info.user.access_hash}</code>
|-Ограничен: <code>{user_info.user.restricted}</code>
|-Верефицирован: <code>{user_info.user.verified}</code>
|-Звонки: <code>{user_info.phone_calls_available}</code>
|-Звонки в личку: <code>{user_info.phone_calls_private}</code>
|-Заблокирован: <code>{user_info.blocked}</code></b>"""
        date_dict.clear()
        await message.edit(user_info)
    except:
        await message.edit("<code>Произошла ошибка...</code>")


modules_help.append(
    {
        "user_info": [
            {
                "inf [reply]/[user id]*": "Ответьте на любое сообщение пользователя чтобы получить информацию"
            },
            {
                "inffull [reply]/[user id]*": "Ответьте на любое сообщение пользователя чтобы получить полную информацию"
            },
        ]
    }
)
