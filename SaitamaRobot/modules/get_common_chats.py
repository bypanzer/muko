import os
from time import sleep

from SaitamaRobot import OWNER_ID, dispatcher
from SaitamaRobot.modules.helper_funcs.extraction import extract_user
from SaitamaRobot.modules.sql.users_sql import get_user_com_chats
from telegram import Update
from telegram.error import BadRequest, RetryAfter, Unauthorized
from telegram.ext import CallbackContext, CommandHandler, Filters
from telegram.ext.dispatcher import run_async


@run_async
def get_user_common_chats(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    msg = update.effective_message
    user = extract_user(msg, args)
    if not user:
        msg.reply_text("Təssüf ki,boşluq ilə heç bir ortaq qrupum yoxdur.")
        return
    common_list = get_user_com_chats(user)
    if not common_list:
        msg.reply_text("Təəssüf ki,bu istifadəçi ilə heç bir ortaq qrupum yoxdur!")
        return
    name = bot.get_chat(user).first_name
    text = f"<b>{name} ilə ortaq qruplarım</b>\n"
    for chat in common_list:
        try:
            chat_name = bot.get_chat(chat).title
            sleep(0.3)
            text += f"• <code>{chat_name}</code>\n"
        except BadRequest:
            pass
        except Unauthorized:
            pass
        except RetryAfter as e:
            sleep(e.retry_after)

    if len(text) < 4096:
        msg.reply_text(text, parse_mode="HTML")
    else:
        with open("ortaq_qruplar.txt", 'w') as f:
            f.write(text)
        with open("ortaq_qruplar.txt", 'rb') as f:
            msg.reply_document(f)
        os.remove("ortaq_qruplar.txt")


COMMON_CHATS_HANDLER = CommandHandler(
    "getchats", get_user_common_chats, filters=Filters.user(OWNER_ID))

dispatcher.add_handler(COMMON_CHATS_HANDLER)
