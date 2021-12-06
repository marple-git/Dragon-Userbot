from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix


@Client.on_message(filters.command("pin", prefix) & filters.me)
async def pin(client: Client, message: Message):
    try:
        message_id = message.reply_to_message.message_id
        await client.pin_chat_message(message.chat.id, message_id)
        await message.edit("<code>Успешно закреплено! </code>")
    except:
        await message.edit(
            "<b>[Ответьте на сообщение которое хотите закрепить]\n</b>"
        )


modules_help.append(
    {"pin": [{"pin": "Закрепить сообщение"}]}
)
