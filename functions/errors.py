import functions.database_manager as db_m
import telegram


def issues(bot, update):
    chat_id = update.message.chat_id
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
