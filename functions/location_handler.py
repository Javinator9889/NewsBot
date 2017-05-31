import functions.database_manager as db_m
import telegram
import os.path as path
import functions.start_handler as st
import urllib.request
import ujson as json


def location(bot, update):
    chat_id = update.message.chat_id
    lat = update.message.location.latitude
    long = update.message.location.longitude
    lang = db_m.read_lang(chat_id)
    if db_m.is_time(chat_id, None) == '1':
        get_time_zone = "https://maps.googleapis.com/maps/api/timezone/json?location={},{}&timestamp=1458000000&key={}".format(
            lat, long, API_KEY_geo)
        open_zone = urllib.request.urlopen(get_time_zone)
        data_zone = open_zone.read()
        zone_data = json.loads(data_zone.decode('utf-8'))
        zone_id = zone_data["timeZoneId"]
        db_m.update_time(chat_id, zone_id)
        db_m.is_time(chat_id, False)
        if lang == 'es':
            bot.sendMessage(chat_id=chat_id,
                            text="Perfecto, hemos actualizado tu *zona horaria* 🌎",
                            parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.sendMessage(chat_id=chat_id,
                            text="Perfect, we have just updated your *time-zone* 🌎",
                            parse_mode=telegram.ParseMode.MARKDOWN)
        if path.exists("first_run_{}".format(chat_id)):
            st.cont_2(bot, update, chat_id)
    else:
        if lang == 'es':
            bot.sendMessage(chat_id,
                            text="Por *motivos de seguridad*, primero _tienes que ir_ a /preferences y luego *actualizar tu zona horaria*",
                            parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.sendMessage(chat_id,
                            text="For *security reasons*, first you _have to go to_ /preferences and then *change your time-zone*",
                            parse_mode=telegram.ParseMode.MARKDOWN)


file_API = open("API-KEY_geo.txt", 'r')
API_KEY_geo = file_API.readline()
file_API.close()
