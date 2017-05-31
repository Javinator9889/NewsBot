import os.path as path
import ujson as json
import urllib.request

import gsearch
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.dispatcher import run_async
from unidecode import unidecode
from urlencode import urlencoder

import functions.database_manager as db_m
import functions.news_keyboard_results as nwk
import functions.prog_updater as p_updater
import functions.update_preferences as up
from functions.keyboards import key_tz


@run_async
def key_lang(bot, update):
    keyboard = [[InlineKeyboardButton("Español 🇪🇸", callback_data='es'),
                 InlineKeyboardButton("English 🇬🇧", callback_data='en')]]

    reply_markup2 = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Elige tu idioma / choose your language:',
                              parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup2)
    return "OK"


@run_async
def echo(bot, update):
    text = update.message['text']
    chat_id = update.message.chat_id
    db_m.r_w_chat_id(chat_id, None)
    lang = db_m.read_lang(chat_id)
    text_dec = unidecode(text)
    url_text = urlencoder(text=text)
    print("Received text:", text, "--Conversion--", text_dec)
    if db_m.is_pref(chat_id, None) == '1':
        print("Changing/adding values to preferences", chat_id)
        up.upd_pref(bot, chat_id, text)
    elif db_m.is_prog(chat_id, None) == '1':
        print("Changing/programming time", chat_id)
        actual = db_m.read_prog(chat_id)
        if actual is None:
            act_list = []
        else:
            act_list = actual.split(",")
        if len(act_list) == 2:
            if lang == 'es':
                bot.sendMessage(chat_id=chat_id,
                                text="Lo sentimos, pero de momento *solo se pueden programar dos horas* 🕖 🕣\n\n_Borra alguna y prueba de nuevo_",
                                parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.sendMessage(chat_id=chat_id,
                                text="We are sorry. Right now, you are able to *set up at most two times* 🕖 🕣\n\n_Delete one and try again_",
                                parse_mode=telegram.ParseMode.MARKDOWN)
            db_m.is_prog(chat_id, False)
        else:
            time = text
            list_from_text = time.split(",")
            print(list_from_text, len(list_from_text))
            if len(list_from_text) == 1 and len(act_list) == 1 or len(list_from_text) == 1 and len(act_list) == 0:
                print("Primera condición (len(list) == 1)")
                next_prog = p_updater.next_day(chat_id, list_from_text[0])
                if next_prog == "Error":
                    if lang == 'es':
                        bot.sendMessage(chat_id,
                                        "El formato de tiempo que has utilizado no es correcto.\n\nUsa /help para saber _cómo programar correctamente el timepo_",
                                        parse_mode=telegram.ParseMode.MARKDOWN)
                    else:
                        bot.sendMessage(chat_id,
                                        "Specified time format is not correct\n\nUse /help to know _how to set up a schedule correctly_",
                                        parse_mode=telegram.ParseMode.MARKDOWN)
                else:
                    print("Next programmation:", next_prog)
                    if len(act_list) == 0:
                        act_list.append(next_prog)
                        print("Final programmation:", act_list[0])
                        db_m.update_prog(chat_id, list_from_text[0])
                        db_m.update_prog_time(act_list[0], chat_id)
                        print("DB updated correctly")
                    else:
                        act_list.append(next_prog)
                        print("Final programmation:", act_list[0], ",", act_list[1])
                        db_m.update_prog(chat_id, list_from_text[0] + "," + db_m.get_time_prog(chat_id))
                        db_m.update_prog_time(act_list[0] + "," + act_list[1], chat_id)
                        print("DB updated correctly")
                    db_m.is_prog(chat_id, False)
                    if lang == 'es':
                        bot.sendMessage(chat_id=chat_id,
                                        text="Perfecto 😄\nLa siguiente programación *comenzará en las próximas 24 horas*",
                                        parse_mode=telegram.ParseMode.MARKDOWN)
                    else:
                        bot.sendMessage(chat_id=chat_id,
                                        text="Perfect 😄\nNext scheduling *will start in the next 24 hours*",
                                        parse_mode=telegram.ParseMode.MARKDOWN)
                    print("Finalizado")
            elif len(list_from_text) == 2:
                print("Segunda condición (len(list) == 2)")
                prog1 = p_updater.next_day(chat_id, list_from_text[0])
                prog2 = p_updater.next_day(chat_id, list_from_text[1])
                if prog1 == "Error" or prog2 == "Error":
                    if lang == 'es':
                        bot.sendMessage(chat_id,
                                        "El formato de tiempo que has utilizado no es correcto.\n\nUsa /help para saber _cómo programar correctamente el timepo_",
                                        parse_mode=telegram.ParseMode.MARKDOWN)
                    else:
                        bot.sendMessage(chat_id,
                                        "Specified time format is not correct\n\nUse /help to know _how to set up a schedule correctly_",
                                        parse_mode=telegram.ParseMode.MARKDOWN)
                else:
                    programming = prog1 + "," + prog2
                    print("Programación final:", programming)
                    db_m.update_prog(chat_id, list_from_text[0] + "," + list_from_text[1])
                    print("Primera base de datos actualizada")
                    db_m.update_prog_time(programming, chat_id)
                    print("Segunda base de datos actualizada")
                    db_m.is_prog(chat_id, False)
                    if lang == 'es':
                        bot.sendMessage(chat_id=chat_id,
                                        text="Perfecto 😄\nLa siguiente programación *comenzará en las próximas 24 horas*",
                                        parse_mode=telegram.ParseMode.MARKDOWN)
                    else:
                        bot.sendMessage(chat_id=chat_id,
                                        text="Perfect 😄\nNext scheduling *will start in the next 24 hours*",
                                        parse_mode=telegram.ParseMode.MARKDOWN)
                    print("Finalizado")
            else:
                print("No se ha cumplido ninguna condición")
                if len(act_list) > 1:
                    if lang == 'es':
                        bot.sendMessage(chat_id=chat_id,
                                        text="Lo sentimos, pero de momento *solo se pueden programar dos horas* 🕖 🕣\n\n_Borra alguna y prueba de nuevo_",
                                        parse_mode=telegram.ParseMode.MARKDOWN)
                    else:
                        bot.sendMessage(chat_id=chat_id,
                                        text="We are sorry. Right now, you are able to *set up at most two times* 🕖 🕣\n\n_Delete one and try again_",
                                        parse_mode=telegram.ParseMode.MARKDOWN)
                    db_m.is_prog(chat_id, False)
                elif lang == 'es':
                    bot.sendMessage(chat_id,
                                    "El formato de tiempo que has utilizado no es correcto.\n\nUsa /help para saber _cómo programar correctamente el timepo_",
                                    parse_mode=telegram.ParseMode.MARKDOWN)
                else:
                    bot.sendMessage(chat_id,
                                    "Specified time format is not correct\n\nUse /help to know _how to set up a schedule correctly_",
                                    parse_mode=telegram.ParseMode.MARKDOWN)
    elif db_m.is_time(chat_id, None) == '1':
        print("Changing/selecting time zone", chat_id)
        search_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(
            url_text[0], API_KEY)
        print("Correctly obtained URL: ", search_url)
        weburl = urllib.request.urlopen(search_url)
        data = weburl.read()
        encoding = weburl.info().get_content_charset('utf-8')
        try:
            obt_data = json.loads(data.decode(encoding))
            print(obt_data)
            latitude = obt_data['results'][0]['geometry']['location']['lat']
            longitude = obt_data['results'][0]['geometry']['location']['lng']
            print("Latitude: ", latitude, " | Longitude: ", longitude)
        except IndexError:
            if lang == 'es':
                bot.sendMessage(chat_id=chat_id,
                                text="La ubicación 🛰 que nos has enviado no existe 😅")
            else:
                bot.sendMessage(chat_id=chat_id,
                                text="The sent 🛰 location does not exist 😅")
        get_time_zone = "https://maps.googleapis.com/maps/api/timezone/json?location={},{}&timestamp=1458000000&key={}".format(
            latitude, longitude, API_KEY_geo)
        print("Correctly obtained TimeZone URL: ", get_time_zone)
        open_zone = urllib.request.urlopen(get_time_zone)
        print("Correctly opened URL")
        data_zone = open_zone.read()
        print("Correctly readed URL data")
        # encoded_zone = data_zone.get_content_charset('utf-8')
        print("Omitted encoding URL-data")
        zone_data = json.loads(data_zone.decode('utf-8'))
        print("Correctly loaded JSON")
        zone_id = zone_data["timeZoneId"]
        print("Correctly obtained \"timeZoneID\": ", zone_id)
        db_m.update_time(chat_id, zone_id)
        key_tz(bot, update, chat_id)
    else:
        if path.exists("first_run_{}".format(chat_id)):
            if lang == 'es':
                bot.sendMessage(chat_id, "¡¡Hey!! Primero tienes que completar la configuración inicial")
            elif lang == 'en':
                bot.sendMessage(chat_id, "Hey!! First you have to finish the initial setup")
            else:
                bot.sendMessage(chat_id, "¡¡Hey!! Primero tienes que completar la configuración inicial\nHey!! First you have to finish the initial setup")
        elif lang == 'es':
            msg = bot.sendMessage(chat_id=chat_id,
                                  text="Recopilando las últimas noticias 📰 en base a tus términos de búsqueda: _\"{}\"_".format(
                                      text_dec),
                                  parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            msg = bot.sendMessage(chat_id=chat_id,
                                  text="Recovering latest news 📰 with your search terms: _\"{}\"_".format(text_dec),
                                  parse_mode=telegram.ParseMode.MARKDOWN)
        mid = msg.message_id
        results = gsearch.search_news(query=text_dec, lang=lang)
        nwk.load_keys(bot, chat_id, results[0], mid)

file_API_KEY = open("API-KEY.txt", 'r')
API_KEY = file_API_KEY.readline()
file_API_KEY.close()

file_API2 = open("API-KEY_geo.txt", 'r')
API_KEY_geo = file_API2.readline()
file_API2.close()
