from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix
from .utils.scripts import restart
import requests
import os
import hashlib


@Client.on_message(filters.command(["modhash", "mh"], prefix) & filters.me)
async def get_mod_hash(client: Client, message: Message):
    if len(message.command) == 1:
        return
    url = message.command[1]
    resp = requests.get(url)
    if not resp.ok:
        await message.edit(
            f"<b>Произошла ошибка во время скачивания модуля <code>{url}</code></b>"
        )
        return
    await message.edit(
        f"<b>Hash модуля: <code>{hashlib.sha256(resp.content).hexdigest()}</code></b>"
    )


@Client.on_message(filters.command(["loadmod", "lm"], prefix) & filters.me)
async def load_mods(client: Client, message: Message):
    if len(message.command) == 1:
        return
    url = message.command[1]

    async def download_mod(content=None):
        if not os.path.exists(f"{os.path.abspath(os.getcwd())}/plugins/custom_modules"):
            os.mkdir(f"{os.path.abspath(os.getcwd())}/plugins/custom_modules")
        code = requests.get(url) if content is None else content
        if not code.ok:
            await message.edit(
                f'<b>Не могу найти модуль <code>{url.split("/")[-1].split(".")[0]}</code></b>'
            )
            return
        with open(f'./plugins/custom_modules/{url.split("/")[-1]}', "wb") as mod:
            mod.write(code.content)
        await message.edit(
            f'<b>Модуль <code>{url.split("/")[-1].split(".")[0]}</code> загружен!</b>'
        )
        await restart()

    if (
        "/".join(url.split("/")[:6])
        == "https://raw.githubusercontent.com/Dragon-Userbot/custom_modules/main"
    ):
        await download_mod()
    elif "/" not in url and "." not in url:
        url = f"https://raw.githubusercontent.com/Dragon-Userbot/custom_modules/main/{url}.py"
        await download_mod()
    else:
        resp = requests.get(url)
        if not resp.ok:
            await message.edit(
                f"<b>Произошла ошибка во время скачивания модуля <code>{url}</code></b>"
            )
            return
        hashes = requests.get(
            "https://raw.githubusercontent.com/Dragon-Userbot/custom_modules/main/modules_hashes.txt"
        ).text
        if hashlib.sha256(resp.content).hexdigest() in hashes:
            await download_mod(resp)
        else:
            await message.edit(
                "<b>Разрешены только <a href=https://github.com/Dragon-Userbot/custom_modules/main/modules_hashes.txt>официальные"
                "</a> модули или модули из <a href=https://github.com/Dragon-Userbot/custom_modules>"
                "репозитория с кастомными модулями</a></b>",
                disable_web_page_preview=True,
            )


@Client.on_message(filters.command(["unloadmod", "ulm"], prefix) & filters.me)
async def unload_mods(client: Client, message: Message):
    if len(message.command) <= 1:
        return
    mod = message.command[1]
    if (
        "/".join(mod.split("/")[:6])
        == "https://raw.githubusercontent.com/Dragon-Userbot/custom_modules/main"
    ):
        mod = "/".join(mod.split("/")[6:]).split(".")[0]

    if os.path.exists(
            f"{os.path.abspath(os.getcwd())}/plugins/custom_modules/{mod}.py"
        ):
        os.remove(f"{os.path.abspath(os.getcwd())}/plugins/custom_modules/{mod}.py")
        await message.edit(f"<b>Модуль <code>{mod}</code> удалён!</b>")
        await restart()

    elif os.path.exists(f"{os.path.abspath(os.getcwd())}/plugins/{mod}.py"):
        await message.edit(
            '<b>Запрещено удалять встроенные модули. Это может сломать Updater</b>'
        )


    else:
        await message.edit(f"<b>Модуль <code>{mod}</code> не найден</b>")


@Client.on_message(filters.command(["loadallmods"], prefix) & filters.me)
async def load_all_mods(clent: Client, message: Message):
    await message.edit("<b>Получаю информацию...</b>")
    if not os.path.exists(f"{os.path.abspath(os.getcwd())}/plugins/custom_modules"):
        os.mkdir(f"{os.path.abspath(os.getcwd())}/plugins/custom_modules")
    modules_list = requests.get(
        "https://api.github.com/repos/Dragon-Userbot/custom_modules/contents/"
    ).json()
    new_modules = {}
    for module_info in modules_list:
        if not module_info["name"].endswith(".py"):
            continue
        if os.path.exists(
            f'{os.path.abspath(os.getcwd())}/plugins/custom_modules/{module_info["name"]}'
        ):
            continue
        new_modules[module_info["name"][:-3]] = module_info["download_url"]
    if not new_modules:
        return await message.edit("<b>All modules already loaded</b>")
    await message.edit(f'<b>Загружаю новые модули: {" ".join(new_modules.keys())}</b>')
    for name, url in new_modules.items():
        with open(f"./plugins/custom_modules/{name}.py", "wb") as f:
            f.write(requests.get(url).content)
    await message.edit(
        f'<b>Успшено загрузил новые модули: {" ".join(new_modules.keys())}</b>'
    )
    await restart()


modules_help.append(
    {
        "loader": [
            {
                "loadmod [link]*": "Скачать модуль\nПоддерживаются моды только из официального репозитория"
            },
            {"unloadmod [module_name]*": "Удалить модуль"},
            {"modhash [link]*": "Получить хэш модуля по ссылке"},
            {"loadallmods": "Загрузить все кастомные модули (на свой страх и риск)"},
        ]
    }
)
