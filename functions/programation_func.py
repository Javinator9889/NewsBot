import functions.database_manager as db_m
import telegram
import functions.look_for_news as lfn


def prog(bot, update, chat_id):
    lang = db_m.read_lang(chat_id)
    print("Recopilando noticias ...\n\n<Programación>")
    if lang == 'es':
        msg = bot.sendMessage(chat_id, "Estamos recopilando las *últimas noticias* 📈... Por favor, espere 🕙",
                              parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        msg = bot.sendMessage(chat_id, "We are looking for the *latest news* 📈... Please, wait 🕙",
                              parse_mode=telegram.ParseMode.MARKDOWN)
    mid = msg.message_id
    lfn.update_news(bot, update, chat_id, mid)
