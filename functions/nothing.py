import telegram  # pip install python-telegram-bot
from telegram.ext.dispatcher import run_async  # python-telegram-bot library
import datetime
import functions.database_manager as db_m


@run_async
def photo(bot, update):  # Function for handling photo-messages
    chat_id = update.message.chat_id
    get_chat_id = db_m.read_chatid(chat_id)
    if get_chat_id is None:
        bot.sendMessage(chat_id,
                        text="*Disculpa las molestias*, pero tienes que _volver a configurar el bot_. Escribe /start o púlsalo" \
                             "\n\n*We are sorry*, but you have to _configure again the bot_. Type /start or press on it",
                        parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        db_m.last_usage(chat_id, datetime.datetime.now().strftime("%H:%M %d-%m-%Y"))
        lang = db_m.read_lang(chat_id)
        print("\tRecibida imagen")
        if lang == 'es':
            bot.sendMessage(chat_id, text="*¡¡NO VEO!!* *¡¡ME HE QUEDADO CIEGO!!*\nAh, no... Que no tengo ojos 😅",
                            parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.sendMessage(chat_id, text="*I CAN'T SEE ANYTHING!!* *I'M BLIND!!*\nAh, no... I have no eyes 😅",
                            parse_mode=telegram.ParseMode.MARKDOWN)


@run_async
def song(bot, update):  # Function for handling audio-messages
    chat_id = update.message.chat_id
    print("\tRecibida canción")
    print("ID: ", chat_id)
    get_chat_id = db_m.read_chatid(chat_id)
    if get_chat_id is None:
        bot.sendMessage(chat_id,
                        text="*Disculpa las molestias*, pero tienes que _volver a configurar el bot_. Escribe /start o púlsalo" \
                             "\n\n*We are sorry*, but you have to _configure again the bot_. Type /start or press on it",
                        parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        db_m.last_usage(chat_id, datetime.datetime.now().strftime("%H:%M %d-%m-%Y"))
        lang = db_m.read_lang(chat_id)
        if lang == 'es':
            bot.sendMessage(chat_id, text="Tienes un gusto horrible... Mejor te envío yo algo 😜",
                            parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.sendMessage(chat_id, text="You have a horrible taste in music... I better send you something 😜",
                            parse_mode=telegram.ParseMode.MARKDOWN)


@run_async
def video(bot, update):  # Function for handling video-messages
    chat_id = update.message.chat_id
    print("\tRecibido vídeo")
    print("ID: ", chat_id)
    get_chat_id = db_m.read_chatid(chat_id)
    if get_chat_id is None:
        bot.sendMessage(chat_id,
                        text="*Disculpa las molestias*, pero tienes que _volver a configurar el bot_. Escribe /start o púlsalo" \
                             "\n\n*We are sorry*, but you have to _configure again the bot_. Type /start or press on it",
                        parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        db_m.last_usage(chat_id, datetime.datetime.now().strftime("%H:%M %d-%m-%Y"))
        lang = db_m.read_lang(chat_id)
        if lang == 'es':
            bot.sendMessage(chat_id,
                            text="Gracias pero yo soy más de cine mudo escocés subtitulado en ruso 😶",
                            parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.sendMessage(chat_id,
                            text="Thank you so much but I prefer Scottish silent movies with Russian subtitles 😶",
                            parse_mode=telegram.ParseMode.MARKDOWN)


@run_async
def voice(bot, update):  # Function for handling voice-messages
    chat_id = update.message.chat_id
    print("\tRecibido audio")
    print("ID: ", chat_id)
    get_chat_id = db_m.read_chatid(chat_id)
    if get_chat_id is None:
        bot.sendMessage(chat_id,
                        text="*Disculpa las molestias*, pero tienes que _volver a configurar el bot_. Escribe /start o púlsalo" \
                             "\n\n*We are sorry*, but you have to _configure again the bot_. Type /start or press on it",
                        parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        db_m.last_usage(chat_id, datetime.datetime.now().strftime("%H:%M %d-%m-%Y"))
        lang = db_m.read_lang(chat_id)
        if lang == 'es':
            bot.sendMessage(chat_id, text="Una voz preciosa, pero particularmente prefiero a _Lady GaGa_ 💃",
                            parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.sendMessage(chat_id, text="What a beautiful voice, but I prefer _Lady GaGa_ 💃",
                            parse_mode=telegram.ParseMode.MARKDOWN)


@run_async
def nothing(bot, update):  # 'nothing' function for unexpected messages (documents, contacts, etc)
    chat_id = update.message.chat_id
    print("ID: ", chat_id)
    get_chat_id = db_m.read_chatid(chat_id)
    if get_chat_id is None:
        bot.sendMessage(chat_id,
                        text="*Disculpa las molestias*, pero tienes que _volver a configurar el bot_. Escribe /start o púlsalo" \
                             "\n\n*We are sorry*, but you have to _configure again the bot_. Type /start or press on it",
                        parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        db_m.last_usage(chat_id, datetime.datetime.now().strftime("%H:%M %d-%m-%Y"))
        lang = db_m.read_lang(chat_id)
        if lang == 'es':
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="No puedo hacer nada con lo que me has enviado 🤔\n\nEscribe /help para obtener ayuda")
        else:
            bot.sendMessage(chat_id,
                            text="I can not do anything with what you have sent me 🤔\n\nType /help to get help")
