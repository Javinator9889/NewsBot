import functions.database_manager as db_m
import telegram
import functions.look_for_news as lfn
import datetime


def prog(bot, update, chat_id):
    lang = db_m.read_lang(chat_id)
    last_msg = db_m.read_last_msgid(chat_id)
    if last_msg is not None:
        try:
            bot.deleteMessage(chat_id=chat_id, message_id=last_msg)
        except telegram.error.BadRequest:
            print("Message to delete not found. Chat_id:", chat_id, "| message_id:", last_msg)
            pass
    print("Recopilando noticias ...\n\n<Programación>", chat_id)
    if lang == 'es':
        msg = bot.sendMessage(chat_id, "Estamos recopilando las *últimas noticias* 📈... Por favor, espere 🕙",
                              parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        msg = bot.sendMessage(chat_id, "We are looking for the *latest news* 📈... Please, wait 🕙",
                              parse_mode=telegram.ParseMode.MARKDOWN)
    mid = msg.message_id
    db_m.last_usage(chat_id, datetime.datetime.now().strftime("%H:%M %d-%m-%Y"))
    lfn.update_news(bot, update, chat_id, mid)
