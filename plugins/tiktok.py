import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message
from utils.utils import modules_help, prefix


@Client.on_message(filters.command("tt", prefix) & filters.me)
async def tiktok(client: Client, message: Message):
    await message.edit('<i>Загрузка...</i>')
    await client.send_message('@ttlessbot', '/start')
    await asyncio.sleep(.5)
    await client.send_message('@ttlessbot', message.reply_to_message.text)
    await asyncio.sleep(1)
    async with asyncio.Lock():
        async for message in client.search_messages(chat_id='ttlessbot', limit=1):
            video = message.video.file_id
    await message.delete()
    await client.send_video(message.chat.id, video)


modules_help.append(
    {
        "tiktok": [
            {
                "tt [reply]*": "Скачать видео из TikTok и отправить его в чат"
            }
        ]
    }
)
