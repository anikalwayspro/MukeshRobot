import html
import json
import re
import random
from time import sleep
import requests
from telegram import (
    CallbackQuery,
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update,
    User,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.utils.helpers import mention_html

import MukeshRobot.modules.sql.chatbot_sql as sql
from MukeshRobot import BOT_ID, BOT_NAME, BOT_USERNAME, dispatcher
from MukeshRobot.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply
from MukeshRobot.modules.log_channel import gloggable
from MukeshAPI import api

@user_admin_no_reply
@gloggable
def mukeshrm(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"rm_chat\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        is_mukesh = sql.set_mukesh(chat.id)
        if is_mukesh:
            is_mukesh = sql.set_mukesh(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"ᴀɪ ᴅɪꜱᴀʙʟᴇᴅ\n"
                f"<b>ᴀᴅᴍɪɴ :</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "{} ᴄʜᴀᴛʙᴏᴛ ᴅɪsᴀʙʟᴇᴅ ʙʏ {}.".format(
                    dispatcher.bot.first_name, mention_html(user.id, user.first_name)
                ),
                parse_mode=ParseMode.HTML,
            )

    return ""


@user_admin_no_reply
@gloggable
def mukeshadd(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"add_chat\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        is_mukesh = sql.rem_mukesh(chat.id)
        if is_mukesh:
            is_mukesh = sql.rem_mukesh(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"ᴀɪ ᴇɴᴀʙʟᴇ\n"
                f"<b>ᴀᴅᴍɪɴ :</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "{} ᴄʜᴀᴛʙᴏᴛ ᴇɴᴀʙʟᴇᴅ ʙʏ {}.".format(
                    dispatcher.bot.first_name, mention_html(user.id, user.first_name)
                ),
                parse_mode=ParseMode.HTML,
            )

    return ""


@user_admin
@gloggable
def mukesh(update: Update, context: CallbackContext):
    message = update.effective_message
    msg = "• ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ᴇɴᴀʙʟᴇ", callback_data="add_chat({})"),
                InlineKeyboardButton(text="ᴅɪsᴀʙʟᴇ", callback_data="rm_chat({})"),
            ],
        ]
    )
    message.reply_text(
        text=msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )


def mukesh_message(context: CallbackContext, message):
    reply_message = message.reply_to_message
    if message.text.lower() == "mukesh":
        return True
    elif BOT_USERNAME in message.text.upper():
        return True
    elif reply_message:
        if reply_message.from_user.id == BOT_ID:
            return True
    else:
        return False


def chatbot(update: Update, context: CallbackContext):
    message = update.effective_message
    chat_id = update.effective_chat.id
    bot = context.bot
    is_mukesh = sql.is_mukesh(chat_id)
    if is_mukesh:
        return

    if message.text and not message.document:
        if not mukesh_message(context, message):
            return
        bot.send_chat_action(chat_id, action="typing")
        url=api.chatgpt(message.text,mode="gf")["results"]
        message.reply_text(url)


async def bot.send_msg(_, message):
    reactions = random.choice(['👍', '❤️', '🔥', '🥰', '👏', '😁', '🤔', '😱', '🎉', '🤩', '🙏', '👌', '🕊', '🤡', '🥴', '😍', '🐳', '❤️‍🔥', '🌚', '💯', '🤣', '🤗', '🫡', '✍️', '🤝', '🙈', '😇', '👀', '👨‍💻', '👻', '💋', '💔', '🤨', '😐', '⚡️', '🏆', '😢', '🍾', '🍓', '😈', '😴', '🤓', '🎃', '🎅', '🎄', '☃️', '💅', '🤪', '🆒', '🗿', '💘', '😘', '💊', '🦄', '🙉', '🙊', '😎', '👾', '🤷‍♂️', '🤷', '🤷‍♀️', '😡
