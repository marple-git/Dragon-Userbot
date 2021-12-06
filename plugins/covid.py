from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix
from .utils.utils import requirements_list

from covid import Covid


@Client.on_message(filters.command("covid", prefix) & filters.me)
async def covid_local(client: Client, message: Message):
    region = " ".join(message.command[1:])
    await message.edit("<code>Data retrieval...</code>")
    covid = Covid(source="worldometers")
    try:
        local_status = covid.get_status_by_country_name(region)
        await message.edit(
            "<b>=======🦠 COVID-19 STATUS 🦠=======</b>\n"
            + f"<b>Регион</b>: <code>{local_status['country']}</code>\n"
            + "<b>====================================</b>\n"
            + f"<b>🤧 Новых случаев</b>: <code>{local_status['new_cases']}</code>\n"
            + f"<b>😷 Новых смертей</b>: <code>{local_status['new_deaths']}</code>\n"
            + "<b>====================================</b>\n"
            + f"<b>😷 Подтверждено</b>: <code>{local_status['confirmed']}</code>\n"
            + f"<b>❗️ Активно:</b> <code>{local_status['active']}</code>\n"
            + f"<b>⚠️ Критичные</b>: <code>{local_status['critical']}</code>\n"
            + f"<b>💀 Смерти</b>: <code>{local_status['deaths']}</code>\n"
            + f"<b>🚑 Излечение</b>: <code>{local_status['recovered']}</code>\n"
        )
    except ValueError:
        await message.edit(f'<code>Нет региона "{region}"</code>')


@Client.on_message(filters.command("regions", prefix) & filters.me)
async def regions(client: Client, message: Message):
    countr = ""
    await message.edit("<code>Получение данных...</code>")
    covid = Covid(source="worldometers")
    regions = covid.list_countries()
    for region in regions:
        region = f"{region}\n"
        countr += region
    await message.edit(f"<code>{countr}</code>")


modules_help.append(
    {
        "covid": [
            {"covid [region]*": "Получить статистику"},
            {
                "regions": "Available regions]\n=======================\n[Worldometer.info statistics are used"
            },
        ]
    }
)

requirements_list.append("covid")
