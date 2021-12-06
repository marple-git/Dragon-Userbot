from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix

from io import StringIO
import sys


@Client.on_message(filters.command(["ex", "py"], prefix) & filters.me)
def user_exec(client: Client, message: Message):
    reply = message.reply_to_message
    code = ""
    try:
        code = reply.text.split(" ", maxsplit=1)[1]
    except IndexError:
        try:
            code = reply.text.split(" \n", maxsplit=1)[1]
        except IndexError:
            pass

    result = sys.stdout = StringIO()
    try:
        exec(code)

        message.edit(
            f"<b>Код:</b>\n"
            f"<code>{code}</code>\n\n"
            f"<b>Результат</b>:\n"
            f"<code>{result.getvalue()}</code>"
        )
    except:
        message.edit(
            f"<b>Код:</b>\n"
            f"<code>{code}</code>\n\n"
            f"<b>Результат</b>:\n"
            f"<code>{sys.exc_info()[0].__name__}: {sys.exc_info()[1]}</code>"
        )


modules_help.append({"python": [{"ex [python code]*": "Выполнить питоновский код"}]})
