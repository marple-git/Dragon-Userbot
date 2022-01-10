from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.chat(-1001200599203))
async def no_garant_provided(client: Client, message: Message):
    text = message.text.lower()
    if (
        'куплю' in text or 'продам' in text or 'приму' in text
    ) and '@getgarantbot' not in text:
        return await client.send_message(-1001200599203, 'Укажи гаранта - @getgarantbot',
                                         reply_to_message_id=message.message_id)
