from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix
from subprocess import Popen, PIPE, TimeoutExpired
from time import perf_counter


@Client.on_message(filters.command(["shell", "sh"], prefix) & filters.me)
async def example_edit(client: Client, message: Message):
    if not message.reply_to_message and len(message.command) == 1:
        return await message.edit(
            "<b>Укажите команду в тексте сообщения или в ответе</b>"
        )
    cmd_text = (
        message.text.split(maxsplit=1)[1]
        if message.reply_to_message is None
        else message.reply_to_message.text
    )
    cmd_obj = Popen(cmd_text, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    await message.edit("<b>Запускаю...</b>")
    text = f"<code>$ {cmd_text}</code>\n\n"
    try:
        start_time = perf_counter()
        stdout, stderr = cmd_obj.communicate(timeout=60)
    except TimeoutExpired:
        text += "<b>Истекло время ожидания (60 секунд)</b>"
    else:
        stop_time = perf_counter()
        if stdout:
            text += "<b>Результат:</b>\n" f"<code>{stdout}</code>\n\n"
        if stderr:
            text += "<b>Ошибка:</b>\n" f"<code>{stderr}</code>\n\n"
        text += f"<b>Завершено за {stop_time - start_time} сек. с кодом {cmd_obj.returncode}</b>"
    await message.edit(text)
    cmd_obj.kill()


modules_help.append(
    {"shell": [{"shell [command]*": "выполнить команду в командной строке"}]}
)
