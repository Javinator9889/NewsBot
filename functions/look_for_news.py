import functions.database_manager as db_m
from telegram.ext.dispatcher import run_async
import gsearch
import functions.news_keyboard_results as nkr
import os
import os.path as path
import datetime


@run_async
def update_news(bot, update, chat_id, message_id):
    pref = db_m.get_pref(chat_id)
    lang = db_m.read_lang(chat_id)
    db_m.last_usage(chat_id, datetime.datetime.now().strftime("%H:%M %d-%m-%Y"))
    if path.exists('dict_out_{}.json'.format(chat_id)):
        os.remove('dict_out_{}.json'.format(chat_id))
    if path.exists('current_{}.txt'.format(chat_id)):
        os.remove('current_{}.txt'.format(chat_id))
    a = pref.split(",")
    b = {}
    total = 0
    try:
        length = len(a)
        max_r = db_m.get_max(chat_id)
        if max_r is None:
            num_res = int(75/length)
        else:
            num_res = int(max_r/length)
        for i in range(0, length):
            addition = i*num_res
            search_results = gsearch.search_news(query=a[i], lang=lang, num=num_res)
            news = search_results[0]
            total += 1
            for u in range(1, num_res):
                try:
                    page = news.get("Page {}".format(u))
                    if page is not None:
                        b["Page {}".format(u+addition)] = page
                        total += 1
                except KeyError:
                    pass
        search_results = {}
        q = 1
        for k, y in b.items():
            if y not in search_results.values() and q <= total:
                current_num = str(q)
                if y is not None:
                    try:
                        key = "Page {}".format(current_num)
                        search_results[key] = y
                        q = q + 1
                    except KeyError:
                        pass
        if len(search_results) < 1:
            if lang == 'es':
                bot.editMessageText(chat_id=chat_id,
                                    text="Tu búsqueda no ha obtenido resultados ❌",
                                    message_id=message_id)
            else:
                bot.editMessageText(chat_id=chat_id,
                                    text="Your search did not get resuls ❌",
                                    message_id=message_id)
        else:
            db_m.last_msgid(chat_id, message_id)
            nkr.load_keys(bot, update, chat_id, search_results, message_id)
    except IndexError:
        pass
