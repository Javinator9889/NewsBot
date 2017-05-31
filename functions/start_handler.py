import os.path as path

import telegram
from telegram.ext.dispatcher import run_async
from unidecode import unidecode

import functions.database_manager as db_m
import functions.look_for_news as lfn
from functions.keyboards import key_lang, key_pref


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
        if msg_id is not None:
            bot.deleteMessage(chat_id=chat_id, message_id=msg_id)
        print("Recopilando noticias ...\n\nIdioma:", lang)
        if lang == 'es':
            msg = bot.sendMessage(chat_id, "Estamos recopilando las *últimas noticias* 📈... Por favor, espere 🕙",
                                  parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            msg = bot.sendMessage(chat_id, "We are looking for the *latest news* 📈... Please, wait 🕙",
                                  parse_mode=telegram.ParseMode.MARKDOWN)
        mid = msg.message_id
        db_m.last_msgid(chat_id, mid)
        lfn.update_news(bot, update, chat_id, mid)


@run_async
def cont_1(bot, update, chat_id, message_id):
    lang = db_m.read_lang(chat_id)
    if lang == 'es':
        bot.editMessageText(chat_id=chat_id, text="Genial 🙌\nAhora que sé en qué idioma buscar tus artículos. \
Ahora necesito que me digas el país donde vives _(esto lo utilizaré para saber\
 a qué hora enviarte las noticias si me programas para ello)_",
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            message_id=message_id)
        bot.sendMessage(chat_id, text="Sencillamente, envíame tu país o la ubicación",
                        parse_mode=telegram.ParseMode.MARKDOWN)
        db_m.is_time(chat_id, True)
    else:
        bot.editMessageText(chat_id=chat_id, text="Great 🙌\nNow that I know in which language I must look for your articles. \
Now I need to know in which country are you _(I'll use this to know when I have to\
 send you news if you want me to that)_",
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            message_id=message_id)
        bot.sendMessage(chat_id, text="Just send me your country or your location",
                        parse_mode=telegram.ParseMode.MARKDOWN)
        db_m.is_time(chat_id, True)
    db_m.is_time(chat_id, True)


@run_async
def cont_2(bot, update, chat_id):
    db_m.is_pref(chat_id, True)
    key_pref(bot, update, chat_id, None)
