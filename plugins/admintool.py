from pyrogram import Client, ContinuePropagation, filters
from pyrogram.types import Message, ChatPermissions
from pyrogram.errors import (
    UserAdminInvalid,
    ChatAdminRequired,
    PeerIdInvalid,
    UsernameInvalid,
)
from pyrogram.raw import functions
from .utils.utils import modules_help, prefix
from .utils.scripts import text, chat_permissions
from time import time
import re
from typing import Dict

from .utils.db import db


@Client.on_message()
async def restrict_users_in_tmute(client: Client, message: Message):
    tmuted_users = db.get("core.ats", f"c{message.chat.id}", [])
    try:
        if message.from_user.id in tmuted_users:
            await message.delete()
    except:
        # Anonymous anal messages
        # Just ignore them
        pass
    raise ContinuePropagation


@Client.on_message(filters.command(["ban"], prefix) & filters.me)
async def ban_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message and message.chat.type not in ["private", "channel"]:
        if message.reply_to_message.from_user:
            try:
                await client.kick_chat_member(
                    message.chat.id, message.reply_to_message.from_user.id
                )
                channel = await client.resolve_peer(message.chat.id)
                user_id = await client.resolve_peer(
                    message.reply_to_message.from_user.id
                )
                if "report_spam" in cause.lower().split():
                    await client.send(
                        functions.channels.ReportSpam(
                            channel=(channel),
                            user_id=(user_id),
                            id=[message.reply_to_message.message_id],
                        )
                    )
                if "delete_history" in cause.lower().split():
                    await client.send(
                        functions.channels.DeleteUserHistory(
                            channel=(channel), user_id=(user_id)
                        )
                    )
                text_c = "".join(
                    f" {_}"
                    for _ in cause.split()
                    if _.lower() not in ["delete_history", "report_spam"]
                )

                await message.edit(
                    f"<b>{message.reply_to_message.from_user.first_name}</b> <code>заблокирован!</code>"
                    + f"\n{'<b>Причина:</b> <i>' + text_c.split(maxsplit=1)[1] + '</i>' if len(text_c.split()) > 1 else ''}"
                )
            except UserAdminInvalid:
                await message.edit("<b>Недостаточно прав</b>")
            except ChatAdminRequired:
                await message.edit("<b>Недостаточно прав</b>")
            except Exception as e:
                print(e)
                await message.edit("<b>Недостаточно прав</b>")
        else:
            await message.edit("<b>Reply on user msg</b>")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                user_to_ban = await client.get_users(cause.split(" ")[1])
                try:
                    await client.kick_chat_member(message.chat.id, user_to_ban.id)
                    await message.edit(
                        f"<b>{user_to_ban.first_name}</b> <code>заблокирован!</code>"
                        + f"\n{'<b>Причина:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("<b>Недостаточно прав</b>")
                except ChatAdminRequired:
                    await message.edit("<b>Недостаточно прав</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>Недостаточно прав</b>")
            except PeerIdInvalid:
                await message.edit("<b>Пользователь не найден</b>")
            except UsernameInvalid:
                await message.edit("<b>Пользователь не найден</b>")
            except IndexError:
                await message.edit("<b>Пользователь не найден</b>")
        else:
            await message.edit("<b>Укажите ID или username</b>")
    else:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["unban"], prefix) & filters.me)
async def unban_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message and message.chat.type not in ["private", "channel"]:
        if message.reply_to_message.from_user:
            try:
                await client.unban_chat_member(
                    message.chat.id, message.reply_to_message.from_user.id
                )
                await message.edit(
                    f"<b>{message.reply_to_message.from_user.first_name}</b> <code>разблокирован!</code>"
                    + f"\n{'<b>Причина:</b> <i>' + cause.split(maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}"
                )
            except UserAdminInvalid:
                await message.edit("<b>Недостаточно прав</b>")
            except ChatAdminRequired:
                await message.edit("<b>Недостаточно прав</b>")
            except Exception as e:
                print(e)
                await message.edit("<b>Недостаточно прав</b>")
        else:
            await message.edit("<b>Reply on user msg</b>")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                user_to_unban = await client.get_users(cause.split(" ")[1])
                try:
                    await client.unban_chat_member(message.chat.id, user_to_unban.id)
                    await message.edit(
                        f"<b>{user_to_unban.first_name}</b> <code>разблокирован</code>"
                        + f"\n{'<b>Причина:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("<b>Недостаточно прав</b>")
                except ChatAdminRequired:
                    await message.edit("<b>Недостаточно прав</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>Недостаточно прав</b>")
            except PeerIdInvalid:
                await message.edit("<b>Пользователь не найден</b>")
            except UsernameInvalid:
                await message.edit("<b>Пользователь не найден</b>")
            except IndexError:
                await message.edit("<b>Пользователь не найден</b>")
        else:
            await message.edit("<b>Укажите ID или username</b>")
    else:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["kick"], prefix) & filters.me)
async def kick_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message and message.chat.type not in ["private", "channel"]:
        if message.reply_to_message.from_user:
            try:
                await client.kick_chat_member(
                    message.chat.id, message.reply_to_message.from_user.id
                )
                await client.unban_chat_member(
                    message.chat.id, message.reply_to_message.from_user.id
                )
                channel = await client.resolve_peer(message.chat.id)
                user_id = await client.resolve_peer(
                    message.reply_to_message.from_user.id
                )
                if "report_spam" in cause.lower().split():
                    await client.send(
                        functions.channels.ReportSpam(
                            channel=(channel),
                            user_id=(user_id),
                            id=[message.reply_to_message.message_id],
                        )
                    )
                if "delete_history" in cause.lower().split():
                    await client.send(
                        functions.channels.DeleteUserHistory(
                            channel=(channel), user_id=(user_id)
                        )
                    )
                text_c = "".join(
                    f" {_}"
                    for _ in cause.split()
                    if _.lower() not in ["delete_history", "report_spam"]
                )

                await message.edit(
                    f"<b>{message.reply_to_message.from_user.first_name}</b> <code>кикнут!</code>"
                    + f"\n{'<b>Причина:</b> <i>' + text_c.split(maxsplit=1)[1] + '</i>' if len(text_c.split()) > 1 else ''}"
                )
            except UserAdminInvalid:
                await message.edit("<b>Недостаточно прав</b>")
            except ChatAdminRequired:
                await message.edit("<b>Недостаточно прав</b>")
            except Exception as e:
                print(e)
                await message.edit("<b>Недостаточно прав</b>")
        else:
            await message.edit("<b>Ответьте на сообщение пользователя</b>")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                user_to_ban = await client.get_users(cause.split(" ")[1])
                try:
                    await client.kick_chat_member(message.chat.id, user_to_ban.id)
                    await client.unban_chat_member(message.chat.id, user_to_ban.id)
                    await message.edit(
                        f"<b>{user_to_ban.first_name}</b> <code>кикнут!</code>"
                        + f"\n{'<b>Причина:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("<b>Недостаточно прав</b>")
                except ChatAdminRequired:
                    await message.edit("<b>Недостаточно прав</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>Недостаточно прав</b>")
            except PeerIdInvalid:
                await message.edit("<b>Пользователь не найден</b>")
            except UsernameInvalid:
                await message.edit("<b>Пользователь не найден</b>")
            except IndexError:
                await message.edit("<b>Пользователь не найден</b>")
        else:
            await message.edit("<b>Укажите ID или username</b>")
    else:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["tmute"], prefix) & filters.me)
async def tmute_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message and message.chat.type not in ["private", "channel"]:
        if message.reply_to_message.from_user:
            if not message.reply_to_message.from_user.is_self:
                tmuted_users = db.get("core.ats", f"c{message.chat.id}", [])
                if message.reply_to_message.from_user.id not in tmuted_users:
                    tmuted_users.append(message.reply_to_message.from_user.id)
                    db.set("core.ats", f"c{message.chat.id}", tmuted_users)
                    await message.edit(
                        f"<b>{message.reply_to_message.from_user.first_name}</b> <code>был замучен (новые сообщения будут удаляться)</code>"
                        + f"\n{'<b>Причина:</b> <i>' + cause.split(maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}"
                    )
                else:
                    await message.edit(
                        f"<b>{message.reply_to_message.from_user.first_name}</b> <code>уже в тмуте</code>"
                    )
            else:
                await message.edit("<b>Нельзя использовать на себе</b>")
        else:
            await message.edit("<b>Reply on user msg</b>")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                user_to_tmute = await client.get_users(cause.split(" ")[1])
                if not user_to_tmute.is_self:
                    tmuted_users = db.get("core.ats", f"c{message.chat.id}", [])
                    if user_to_tmute.id not in tmuted_users:
                        tmuted_users.append(user_to_tmute.id)
                        db.set("core.ats", f"c{message.chat.id}", tmuted_users)
                        await message.edit(
                            f"<b>{user_to_tmute.first_name}</b> <code>был замучен (новые сообщения будут удаляться)</code>"
                            + f"\n{'<b>Причина:</b> <i>' + cause.split(maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                        )
                    else:
                        await message.edit(
                            f"<b>{user_to_tmute.first_name}</b> <code>уже в тмуте</code>"
                        )
                else:
                    await message.edit("<b>Нельзя использовать на себе</b>")
            except PeerIdInvalid:
                await message.edit("<b>Пользователь не найден</b>")
            except UsernameInvalid:
                await message.edit("<b>Пользователь не найден</b>")
            except IndexError:
                await message.edit("<b>Пользователь не найден</b>")
        else:
            await message.edit("<b>Укажите ID или username</b>")
    else:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["tunmute"], prefix) & filters.me)
async def tunmute_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message and message.chat.type not in ["private", "channel"]:
        if message.reply_to_message.from_user:
            if not message.reply_to_message.from_user.is_self:
                tmuted_users = db.get("core.ats", f"c{message.chat.id}", [])
                if message.reply_to_message.from_user.id not in tmuted_users:
                    await message.edit(
                        f"<b>{message.reply_to_message.from_user.first_name}</b> <code>не в тмуте</code>"
                    )
                else:
                    tmuted_users.remove(message.reply_to_message.from_user.id)
                    db.set("core.ats", f"c{message.chat.id}", tmuted_users)
                    await message.edit(
                        f"<b>{message.reply_to_message.from_user.first_name}</b> <code>был размучен (сообщения больше не удаляются)</code>"
                        + f"\n{'<b>Cause:</b> <i>' + cause.split(maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}"
                    )
            else:
                await message.edit("<b>Нельзя использовать на себе</b>")
        else:

            await message.edit("<b>Ответьте на сообщение пользователя</b>")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                user_to_tunmute = await client.get_users(cause.split(" ")[1])
                if not user_to_tunmute.is_self:
                    tmuted_users = db.get("core.ats", f"c{message.chat.id}", [])
                    if user_to_tunmute.id not in tmuted_users:
                        await message.edit(
                            f"<b>{user_to_tunmute.first_name}</b> <code>не в тмуте</code>"
                        )
                    else:
                        tmuted_users.remove(user_to_tunmute.id)
                        db.set("core.ats", f"c{message.chat.id}", tmuted_users)
                        await message.edit(
                            f"<b>{user_to_tunmute.first_name}</b> <code>был размучен (сообщения больше не удаляются)</code>"
                            + f"\n{'<b>Причина:</b> <i>' + cause.split(maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                        )
                else:
                    await message.edit("<b>Нельзя использовать на себе</b>")
            except PeerIdInvalid:
                await message.edit("<b>Пользователь не найден</b>")
            except UsernameInvalid:
                await message.edit("<b>Пользователь не найден</b>")
            except IndexError:
                await message.edit("<b>Пользователь не найден</b>")
        else:
            await message.edit("<b>Укажите ID или username</b>")
    else:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["tmute_users"], prefix) & filters.me)
async def tunmute_users_command(client: Client, message: Message):
    if message.chat.type not in ["private", "channel"]:
        text = f"<b>Все пользователи</b> <code>{message.chat.title}</code> <b>в тмуте</b>\n\n"
        count = 0
        tmuted_users = db.get("core.ats", f"c{message.chat.id}", [])
        for user in tmuted_users:
            try:
                _name_ = await client.get_users(user)
                count += 1
                text += f"{count}. <b>{_name_.first_name}</b>\n"
            except PeerIdInvalid:
                pass
        if count == 0:
            await message.edit("<b>Нет пользователей в тмуте</b>")
        else:
            text += f"\n<b>Всего пользователей в тмуте</b> {count}"
            await message.edit(text)
    else:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["unmute"], prefix) & filters.me)
async def unmute_command(client, message):
    cause = await text(client, message)
    if message.reply_to_message and message.chat.type not in ["private", "channel"]:
        u_p = await chat_permissions(client, message)
        if message.reply_to_message.from_user:
            try:
                await client.restrict_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    u_p,
                    int(time() + 30),
                )
                await message.edit(
                    f"<b>{message.reply_to_message.from_user.first_name}</b> <code>размучен</code>"
                    + f"\n{'<b>Причина:</b> <i>' + cause.split(' ', maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}"
                )
            except UserAdminInvalid:
                await message.edit("<b>Недостаточно прав</b>")
            except ChatAdminRequired:
                await message.edit("<b>Недостаточно прав</b>")
            except Exception as e:
                print(e)
                await message.edit("<b>Недостаточно прав</b>")
        else:
            await message.edit("<b>Ответьте на сообщение юзера чтобы использовать это</b>")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        u_p = await chat_permissions(client, message)
        if len(cause.split()) > 1:
            try:
                user_to_unmute = await client.get_users(cause.split(" ")[1])
                try:
                    await client.restrict_chat_member(
                        message.chat.id, user_to_unmute.id, u_p, int(time() + 30)
                    )
                    await message.edit(
                        f"<b>{user_to_unmute.first_name}</b> <code>размучен!</code>"
                        + f"\n{'<b>Причина:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("<b>Недостаточно прав</b>")
                except ChatAdminRequired:
                    await message.edit("<b>Недостаточно прав</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>Недостаточно прав</b>")
            except PeerIdInvalid:
                await message.edit("<b>Пользователь не найден</b>")
            except UsernameInvalid:
                await message.edit("<b>Пользователь не найден</b>")
            except IndexError:
                await message.edit("<b>Пользователь не найден</b>")
        else:
            await message.edit("<b>Укажите ID или username</b>")
    else:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["mute"], prefix) & filters.me)
async def mute_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message and message.chat.type not in ["private", "channel"]:
        mute_seconds: int = 0
        for character in "mhdw":
            match = re.search(rf"(\d+|(\d+\.\d+)){character}", message.text)
            if match:
                if character == "m":
                    mute_seconds += int(
                        float(match.string[match.start() : match.end() - 1]) * 60 // 1
                    )
                if character == "h":
                    mute_seconds += int(
                        float(match.string[match.start() : match.end() - 1]) * 3600 // 1
                    )
                if character == "d":
                    mute_seconds += int(
                        float(match.string[match.start() : match.end() - 1])
                        * 86400
                        // 1
                    )
                if character == "w":
                    mute_seconds += int(
                        float(match.string[match.start() : match.end() - 1])
                        * 604800
                        // 1
                    )
        try:
            if mute_seconds > 30:
                await client.restrict_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    ChatPermissions(),
                    int(time()) + mute_seconds,
                )
                from_user = message.reply_to_message.from_user
                mute_time: Dict[str, int] = {
                    "days": mute_seconds // 86400,
                    "hours": mute_seconds % 86400 // 3600,
                    "minutes": mute_seconds % 86400 % 3600 // 60,
                }
                message_text = (
                    f"<b>{from_user.first_name}</b> <code> был замучен на"
                    f" {((str(mute_time['days']) + ' дн.') if mute_time['days'] > 0 else '')}"
                    f" {((str(mute_time['hours']) + ' ч.') if mute_time['hours'] > 0 else '')}"
                    f" {((str(mute_time['minutes']) + ' мин.') if mute_time['minutes'] > 0 else '')}</code>"
                    + f"\n{'<b>Причина:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''} "
                )
                while "  " in message_text:
                    message_text = message_text.replace("  ", " ")
            else:
                await client.restrict_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    ChatPermissions(),
                )
                message_text = (
                    f"<b>{message.reply_to_message.from_user.first_name}</b> <code> был навсегда замучен</code>"
                    + f"\n{'<b>Причина:</b> <i>' + cause.split(' ', maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}"
                )
            await message.edit(message_text)
        except UserAdminInvalid:
            await message.edit("<b>Недостаточно прав</b>")
        except ChatAdminRequired:
            await message.edit("<b>Недостаточно прав</b>")
        except Exception as e:
            print(e)
            await message.edit("<b>Недостаточно прав</b>")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                user_to_unmute = await client.get_users(cause.split(" ")[1])
                mute_seconds: int = 0
                for character in "mhdw":
                    match = re.search(rf"(\d+|(\d+\.\d+)){character}", message.text)
                    if match:
                        if character == "m":
                            mute_seconds += int(
                                float(match.string[match.start() : match.end() - 1])
                                * 60
                                // 1
                            )
                        if character == "h":
                            mute_seconds += int(
                                float(match.string[match.start() : match.end() - 1])
                                * 3600
                                // 1
                            )
                        if character == "d":
                            mute_seconds += int(
                                float(match.string[match.start() : match.end() - 1])
                                * 86400
                                // 1
                            )
                        if character == "w":
                            mute_seconds += int(
                                float(match.string[match.start() : match.end() - 1])
                                * 604800
                                // 1
                            )
                try:
                    if mute_seconds > 30:
                        await client.restrict_chat_member(
                            message.chat.id,
                            user_to_unmute.id,
                            ChatPermissions(),
                            int(time()) + mute_seconds,
                        )
                        mute_time: Dict[str, int] = {
                            "days": mute_seconds // 86400,
                            "hours": mute_seconds % 86400 // 3600,
                            "minutes": mute_seconds % 86400 % 3600 // 60,
                        }
                        message_text = (
                            f"<b>{user_to_unmute.first_name}</b> <code> был замучен на"
                            f" {((str(mute_time['days']) + ' дн.') if mute_time['days'] > 0 else '')}"
                            f" {((str(mute_time['hours']) + ' ч.') if mute_time['hours'] > 0 else '')}"
                            f" {((str(mute_time['minutes']) + ' м.') if mute_time['minutes'] > 0 else '')}</code>"
                            + f"\n{'<b>Причина:</b> <i>' + cause.split(' ', maxsplit=3)[3] + '</i>' if len(cause.split()) > 3 else ''}"
                        )
                        while "  " in message_text:
                            message_text = message_text.replace("  ", " ")
                    else:
                        await client.restrict_chat_member(
                            message.chat.id, user_to_unmute.id, ChatPermissions()
                        )
                        message_text = (
                            f"<b>{user_to_unmute.first_name}</b> <code> был навсегда замучен</code>"
                            + f"\n{'<b>Причина:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                        )
                    await message.edit(message_text)
                except UserAdminInvalid:
                    await message.edit("<b>Недостаточно прав</b>")
                except ChatAdminRequired:
                    await message.edit("<b>Недостаточно прав</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>Недостаточно прав</b>")
            except PeerIdInvalid:
                await message.edit("<b>Пользователь не найден</b>")
            except UsernameInvalid:
                await message.edit("<b>Пользователь не найден</b>")
            except IndexError:
                await message.edit("<b>Пользователь не найден</b>")
        else:
            await message.edit("<b>Укажите ID или username/b>")
    else:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["demote"], prefix) & filters.me)
async def demote_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message and message.chat.type not in ["private", "channel"]:
        if message.reply_to_message.from_user:
            try:
                await client.promote_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    is_anonymous=False,
                    can_manage_chat=False,
                    can_change_info=False,
                    can_post_messages=False,
                    can_edit_messages=False,
                    can_delete_messages=False,
                    can_restrict_members=False,
                    can_invite_users=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                    can_manage_voice_chats=False,
                )
                await message.edit(
                    f"<b>{message.reply_to_message.from_user.first_name}</b> <code>понижен!</code>"
                    + f"\n{'<b>Причина:</b> <i>' + cause.split(' ', maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}"
                )
            except UserAdminInvalid:
                await message.edit("<b>Недостаточно прав</b>")
            except ChatAdminRequired:
                await message.edit("<b>Недостаточно прав</b>")
            except Exception as e:
                print(e)
                await message.edit("<b>Недостаточно прав</b>")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                promote_user = await client.get_users(cause.split(" ")[1])
                try:
                    await client.promote_chat_member(
                        message.chat.id,
                        promote_user.id,
                        is_anonymous=False,
                        can_manage_chat=False,
                        can_change_info=False,
                        can_post_messages=False,
                        can_edit_messages=False,
                        can_delete_messages=False,
                        can_restrict_members=False,
                        can_invite_users=False,
                        can_pin_messages=False,
                        can_promote_members=False,
                        can_manage_voice_chats=False,
                    )
                    await message.edit(
                        f"<b>{promote_user.first_name}</b> <code>понижен!</code>"
                        + f"\n{'<b>Причина:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("<b>Недостаточно прав</b>")
                except ChatAdminRequired:
                    await message.edit("<b>Недостаточно прав</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>Недостаточно прав</b>")
            except PeerIdInvalid:
                await message.edit("<b>Пользователь не найден/b>")
            except UsernameInvalid:
                await message.edit("<b>Пользователь не найден</b>")
            except IndexError:
                await message.edit("<b>Пользователь не найден</b>")
        else:
            await message.edit("<b>Укажите ID или username</b>")
    else:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["promote"], prefix) & filters.me)
async def promote_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message and message.chat.type not in ["private", "channel"]:
        if message.reply_to_message.from_user:
            try:
                await client.promote_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    can_delete_messages=True,
                    can_restrict_members=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                )
                if len(cause.split()) > 1:
                    await client.set_administrator_title(
                        message.chat.id,
                        message.reply_to_message.from_user.id,
                        cause.split(maxsplit=1)[1],
                    )
                await message.edit(
                    f"<b>{message.reply_to_message.from_user.first_name}</b> <code>повышен!</code>"
                    + f"\n{'<b>Префикс:</b> <i>' + cause.split(' ', maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}"
                )
            except UserAdminInvalid:
                await message.edit("<b>Недостаточно прав</b>")
            except ChatAdminRequired:
                await message.edit("<b>Недостаточно прав</b>")
            except Exception as e:
                print(e)
                await message.edit("<b>Недостаточно прав</b>")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                promote_user = await client.get_users(cause.split(" ")[1])
                try:
                    await client.promote_chat_member(
                        message.chat.id,
                        promote_user.id,
                        can_delete_messages=True,
                        can_restrict_members=True,
                        can_invite_users=True,
                        can_pin_messages=True,
                    )
                    if len(cause.split()) > 1:
                        await client.set_administrator_title(
                            message.chat.id,
                            promote_user.id,
                            f"\n{cause.split(' ', maxsplit=2)[2] if len(cause.split()) > 2 else None}",
                        )
                    await message.edit(
                        f"<b>{promote_user.first_name}</b> <code>повышен!</code>"
                        + f"\n{'<b>Префикс:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("<b>Недостаточно прав</b>")
                except ChatAdminRequired:
                    await message.edit("<b>Недостаточно прав</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>Недостаточно прав</b>")
            except PeerIdInvalid:
                await message.edit("<b>Пользователь не найден</b>")
            except UsernameInvalid:
                await message.edit("<b>Пользователь не найден</b>")
            except IndexError:
                await message.edit("<b>Пользователь не найден</b>")
        else:
            await message.edit("<b>Укажите ID или username</b>")
    else:
        await message.edit("<b>Unsupported</b>")


modules_help.append(
    {
        "admintool": [
            {
                "ban [reply]/[userid]* [reason] [report_spam] [delete_history]": "Забанить юзера в чате"
            },
            {
                "unban [reply]/[userid]* [reason] [report_spam] [delete_history]": "Разбанить юзера в чате"
            },
            {
                "kick [reply]/[userid]* [reason] [report_spam] [delete_history]": "Кикнуть юзера из чата"
            },
            {
                "tmute [reply]/[userid]* [reason]": "Удалить все новые сообщения от юзера из чата"
            },
            {
                "tunmute [reply]/[userid]* [reason]": "Прекратить удалять все новые сообщения от юзера из чата"
            },
            {
                "tmute_users": "Список пользователей, чьи сообщения автоматически удаляются"
            },
            {
                "mute [reply]/[userid]* [reason] [1m]/[1h]/[1d]/[1w]": "Замутить пользователя в чате"
            },
            {"unmute [reply]/[userid]* [reason]": "Размутить юзера в чате"},
            {"promote [reply]/[userid]* [prefix]": "Повысить юзера в чате"},
            {"demote [reply]/[userid]* [reason]": "Понизить юзера в чате"},
        ]
    }
)
