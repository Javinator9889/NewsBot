import telegram
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import functions.database_manager as db_m
import functions.start_handler as start
import os.path as path
from functions.keyboards import *


@run_async
def help_handler(bot, update):
    chat_id = update.message.chat_id
    lang = db_m.read_lang(chat_id)
    print(lang)
    if db_m.is_time(chat_id, None) == '1':
        if lang == 'es':
            bot.sendMessage(chat_id=chat_id,
                                text="En esta parte, envíanos *el nombre de tu país* o bien *tu ubicación*." \
                                "\nDe esta manera podremos enviarte artículos y noticias si nos lo programas",
                                parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.sendMessage(chat_id=chat_id,
                                text="Now, send us *your country name* or your *location*. "\
                                "\nWith this, we will be able to send you articles and news if you schedule that",
                                parse_mode=telegram.ParseMode.MARKDOWN)
    elif db_m.is_pref(chat_id, None) == '1':
        key_two(bot, update, chat_id, lang, None)
    elif db_m.is_prog(chat_id, None) == '1':
        key_four(bot, update, chat_id, lang, None)
    else:
        main_menu(bot, update, chat_id, None, lang)
