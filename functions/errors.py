import functions.database_manager as db_m
import datetime
import telegram


def issues(bot, update):
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
        if lang == 'es':
            bot.sendMessage(chat_id=chat_id,
                            text="ᴘʀᴏʙʟᴇᴍᴀs ᴄᴏɴᴏᴄɪᴅᴏs\n\n*1.* *No aparecen algunas de mis preferencias* ❌ al usar /start. " \
                            "*Google* tiene una política de servicio muy estricta 👮 y limita los resultados que recoge el bot." \
                            " *Para solucionarlo*, lo mejor es eliminar todas las preferencias y añadir solo " \
                            "*palabras clave*, sin utilizar _trucos de búsqueda_",
                            parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.sendMessage(chat_id=chat_id,
                            text="ᴋɴᴏᴡɴ ɪssᴜᴇs\n\n*1.* *There is no results of my preferences* ❌ while using /start. " \
                            "*Google* has a very strict usage policy 👮 and limit bot results. For *solving it*, the best " \
                            "option is deleting all preferences and add only *keywords*, without using _search tricks_",
                            parse_mode=telegram.ParseMode.MARKDOWN)
