import telegram
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import functions.database_manager as db_m
import datetime
import os.path as path


@run_async
def key_pref(bot, update):
    chat_id = update.message.chat_id
    get_chat_id = db_m.read_chatid(chat_id)
    if get_chat_id is None:
        bot.sendMessage(chat_id,
                        text="*Disculpa las molestias*, pero tienes que _volver a configurar el bot_. Escribe /start o púlsalo" \
                             "\n\n*We are sorry*, but you have to _configure again the bot_. Type /start or press on it",
                        parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        lang = db_m.read_lang(chat_id)
        db_m.last_usage(chat_id, datetime.datetime.now().strftime("%H:%M %d-%m-%Y"))
        if lang == 'es':
            zone = "Zona horaria 🕙"
            time = "Idioma 🗣"
            pref = "Preferencias ⚙"
            prog = "Programación 📅"
            res = "Número de resultados 📚"
        else:
            zone = "Time zone 🕙"
            time = "Language 🗣"
            pref = "Preferences ⚙"
            prog = "Time scheduling 📅"
            res = "Number of results 📚"
        keyboard = [[InlineKeyboardButton(zone, callback_data='tz'), InlineKeyboardButton(time, callback_data='lang')],
                    [InlineKeyboardButton(pref, callback_data='lista'), InlineKeyboardButton(prog, callback_data='prog')],
                    [InlineKeyboardButton(res, callback_data='max')]]

        reply_markup2 = InlineKeyboardMarkup(keyboard)

        if path.exists("first_run_{}".format(chat_id)):
            bot.sendMessage(chat_id=chat_id,
                            text="¡Hey! Primero tienes que terminar la configuración inicial\n\nHey! first you have to finish the initial setup")
        elif lang == 'es':
            bot.sendMessage(chat_id=chat_id,
                            text='¿Qué quieres actualizar? Pulsa encima de la opción que quieras',
                            parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup2)
        else:
            bot.sendMessage(chat_id=chat_id,
                            text='What do you want to update? Press on the option you want to change',
                            reply_markup=reply_markup2)
        return "OK"
