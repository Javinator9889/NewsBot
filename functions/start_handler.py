import os.path as path

import telegram
from telegram.ext.dispatcher import run_async
from unidecode import unidecode

import functions.database_manager as db_m
import functions.look_for_news as lfn
from functions.keyboards import key_lang, key_pref
import datetime


@run_async
def start(bot, update):
    chat_id = update.message.chat_id
    user = unidecode(update.message.from_user['first_name'])
    print("Executing '/start' ...", chat_id)
    if db_m.r_w_chat_id(chat_id, user) == "Updated":
        print("\nFirst run", chat_id)
        first_boot = open("first_run_{}".format(chat_id), 'w')
        first_boot.close()
        key_lang(bot, update)
    elif path.exists("first_run_{}".format(chat_id)):
        bot.sendMessage(chat_id,
                        "¡¡Hey!! Primero tienes que completar la configuración inicial\nHey!! First you have to finish the initial setup")
    else:
        lang = db_m.read_lang(chat_id)
        msg_id = db_m.read_last_msgid(chat_id)
        db_m.last_usage(chat_id, datetime.datetime.now().strftime("%H:%M %d-%m-%Y"))
        try:
            if msg_id is not None:
                bot.deleteMessage(chat_id=chat_id, message_id=msg_id)
        except telegram.error.BadRequest:
            print("No message found for chat_id:", chat_id)
            pass
        print("Recopilando noticias ...\n\nIdioma:", lang)
        url = 'https://goo.gl/60ECGQ'
        url2 = 'https://goo.gl/fFOI2j'
        act = db_m.get_pref(chat_id)
        if act is None or act == '':
            if lang == 'es':
                bot.sendMessage(chat_id, "Mmm... Me temo que va a ser complicado buscar algo sino sé tus preferencias\n" \
                                "Ejecuta /config para establecer tus gustos")
            else:
                bot.sendMessage(chat_id, "Mmm... I think it's going to be difficult looking for something if I don't " \
                                "know your preferences\nExecute /config for setting your pleasures")
            db_m.last_msgid(chat_id, None)
        elif lang == 'es':
            bot.sendMessage(chat_id, "¿Te gusta este bot?\n*Compártelo* 🗣 y *puntúalo* 🌟 [en este enlace 🔗]("+url+") \no [👉 directamente desde aquí 👈]("+url2+")",
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            disable_web_page_preview=True)
            msg = bot.sendMessage(chat_id, "Estamos recopilando las *últimas noticias* 📈... Por favor, espere 🕙",
                                  parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.sendMessage(chat_id,
                            "Do you like this bot?\n*Share it* 🗣 & *rate it* 🌟 [using this link 🔗]("+url+") \nor [👉 directly from here 👈]("+url2+")",
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            disable_web_page_preview=True)
            msg = bot.sendMessage(chat_id, "We are looking for the *latest news* 📈... Please, wait 🕙",
                                  parse_mode=telegram.ParseMode.MARKDOWN)
        mid = msg.message_id
        lfn.update_news(bot, update, chat_id, mid)


@run_async
def cont_1(bot, update, chat_id, message_id):
    lang = db_m.read_lang(chat_id)
    db_m.last_usage(chat_id, datetime.datetime.now().strftime("%H:%M %d-%m-%Y"))
    if lang == 'es':
        bot.editMessageText(chat_id=chat_id, text="Genial 🙌\nAhora que sé en qué idioma buscar tus artículos, \
dime en qué país vives. También puedes enviarme *tu ubicación* 🛰",
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            message_id=message_id)
        db_m.is_time(chat_id, True)
    else:
        bot.editMessageText(chat_id=chat_id, text="Great 🙌\nNow that I know in which language I must look for your articles, \
tell me where are you living. Also you can send me *your location* 🛰",
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            message_id=message_id)
        db_m.is_time(chat_id, True)
    db_m.is_time(chat_id, True)


@run_async
def cont_2(bot, update, chat_id):
    db_m.last_usage(chat_id, datetime.datetime.now().strftime("%H:%M %d-%m-%Y"))
    db_m.is_pref(chat_id, True)
    key_pref(bot, update, chat_id, None)
