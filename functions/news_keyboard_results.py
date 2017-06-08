import telegram
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import ujson as json
import functions.database_manager as db_m
from functions.title_finder import title as title_finder
import datetime


@run_async
def key_one(bot, update, chat_id, message_id):
    input_data = open('dict_out_{}.json'.format(chat_id), 'rb')
    json_data = json.load(input_data)
    a = 1
    current_val = open('current_{}.txt'.format(chat_id), 'w')
    current_val.write(str(a))
    current_val.close()

    lang = db_m.read_lang(chat_id)
    db_m.last_usage(chat_id, datetime.datetime.now().strftime("%H:%M %d-%m-%Y"))
    url = json_data["Page {}".format(a)]
    if url is None:
        if db_m.read_lang(chat_id) == 'es':
            bot.sendMessage(chat_id=chat_id,
                            text="Tu búsqueda no ha obtenido resultados")
            msg_id = db_m.read_last_msgid(chat_id)
            if msg_id is not None:
                bot.deleteMessage(chat_id=chat_id, message_id=msg_id)
            db_m.last_msgid(chat_id, None)
        else:
            bot.sendMessage(chat_id=chat_id, text="Your search has no results")
    else:
        title = title_finder(url)
        if lang == 'es':
            keyboard = [[InlineKeyboardButton("Leer más 📖", url=url),
                         InlineKeyboardButton("Siguiente 📰", callback_data='next1')]]
        else:
            keyboard = [[InlineKeyboardButton("Read more 📖", url=url),
                         InlineKeyboardButton("Next 📰", callback_data='next1')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        bot.editMessageText(chat_id=chat_id, text="*{}*\n[Link 🔗]({})".format(title, url),
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            reply_markup=reply_markup,
                            message_id=message_id)
        # db_m.last_msgid(chat_id, message_id)
    return "OK"


@run_async
def key_var(bot, update, chat_id, message_id, n_or_p):
    input_data = open('dict_out_{}.json'.format(chat_id), 'rb')
    json_data = json.load(input_data)
    current_val = open('current_{}.txt'.format(chat_id), 'r')
    read_value = current_val.readline()
    current_val.close()

    if n_or_p is True:
        a = int(read_value) + 1
    else:
        a = int(read_value) - 1

    new_val = open('current_{}.txt'.format(chat_id), 'w')
    new_val.write(str(a))
    new_val.close()

    lang = db_m.read_lang(chat_id)
    db_m.last_usage(chat_id, datetime.datetime.now().strftime("%H:%M %d-%m-%Y"))
    url = json_data["Page {}".format(a)]
    print("Reading value:", a, "URL:", url)
    title = title_finder(url)
    try:
        json_data["Page {}".format(a-1)]
        if lang == 'es':
            prev = "◀ Anterior"
        else:
            prev = "◀ Previous"
    except KeyError:
        prev = None
    try:
        json_data["Page {}".format(a+1)]
        if lang == 'es':
            nxt = "Siguiente 📰"
        else:
            nxt = "Next 📰"
    except KeyError:
        nxt = None
    if lang == 'es':
        destination = "Leer más 📖"
    else:
        destination = "Read more 📖"
    if nxt is None:
        keyboard = [[InlineKeyboardButton(prev, callback_data='prev'),
                     InlineKeyboardButton(destination, url=url)]]
    elif prev is None:
        keyboard = [[InlineKeyboardButton(destination, url=url),
                     InlineKeyboardButton(nxt, callback_data='next')]]
    else:
        keyboard = [[InlineKeyboardButton(prev, callback_data='prev'),
                     InlineKeyboardButton(destination, url=url),
                     InlineKeyboardButton(nxt, callback_data='next')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.editMessageText(chat_id=chat_id, text="*{}*\n[Link 🔗]({})".format(title, url),
                        parse_mode=telegram.ParseMode.MARKDOWN,
                        reply_markup=reply_markup,
                        message_id=message_id)
    return "OK"


@run_async
def load_keys(bot, update, chat_id, dictionary, message_id):
    json_str = json.dumps(dictionary, ensure_ascii=False, indent=4)
    bytes_obj = json_str.encode()
    file = open('dict_out_{}.json'.format(chat_id), 'wb')
    file.write(bytes_obj)
    file.close()
    db_m.last_usage(chat_id, datetime.datetime.now().strftime("%H:%M %d-%m-%Y"))
    key_one(bot, update, chat_id, message_id)
