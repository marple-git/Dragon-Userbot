from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix
import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}


@Client.on_message(filters.command("course", prefix) & filters.me)
async def convert(client: Client, message: Message):
    try:
        await message.edit("<code>Получение данных...</code>")
        name = message.command[1]

        if name == "btc":
            name = "1₿"
            link = 'https://ru.investing.com/crypto/bitcoin'
        else:
            link = f"https://ru.investing.com/currencies/{name}-rub"

        full_page = requests.get(link, headers=headers, timeout=3)
        soup = BeautifulSoup(full_page.content, "html.parser")
        rub = soup.find("span", id="last_last")
        await message.edit(f"<b>{name} сейчас стоит </b><code> {rub} </code><b> руб</b>")
    except:
        await message.edit("<code>Ошибка</code>")


modules_help.append(
    {
        "course": [
            {
                "course [валюта]*": "Конвертер в рубли из любой валюты\nНе использовать чаще 10 раз в минуту"
            }
        ]
    }
)
