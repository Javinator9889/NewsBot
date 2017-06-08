import functions.database_manager as db_m
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import telegram
import os.path as path
import datetime


def develop(bot, update):
    chat_id = update.message.chat_id
    print("Executing /develop")
    url1 = 'https://goo.gl/K7vs1z'
    url2 = 'https://goo.gl/60ECGQ'
    get_chat_id = db_m.read_chatid(chat_id)
    if get_chat_id is None:
        bot.sendMessage(chat_id,
                        text="*Disculpa las molestias*, pero tienes que _volver a configurar el bot_. Escribe /start o púlsalo" \
                        "\n\n*We are sorry*, but you have to _configure again the bot_. Type /start or press on it",
                        parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        db_m.last_usage(chat_id, datetime.datetime.now().strftime("%H:%M %d-%m-%Y"))
        lang = db_m.read_lang(chat_id)
        if path.exists("first_run_{}".format(chat_id)):
            bot.sendMessage(chat_id=chat_id,
                            text="¡Hey! Primero tienes que terminar la configuración inicial\n\nHey! first you have to finish the initial setup")
        elif lang == 'es':
            keyboard = [[InlineKeyboardButton("Ir al proyecto 👁", url=url1),
                         InlineKeyboardButton("Apoya este bot 🌟", url=url2)]]
            rp_mk = InlineKeyboardMarkup(keyboard)
            bot.sendMessage(chat_id=chat_id,
                            text="_¿Eres desarrollador? 🤓 ¿Te interesa aprender? 📚_ *Estás en el lugar indicado*."\
                            "\n\nNuestra política (_basada en la de Telegram_) confía en los proyectos *OpenSource* (de "\
                            "código libre) 📖 y, por lo tanto, este bot es *completamente público* 👏\nPuedes acceder al"\
                            " [proyecto en GitHub 🔗](https://github.com/Javinator9889/NewsBot) y ver cómo lo hemos hecho."\
                            " Está escrito *en Python 3* y en el proyecto tienes una *lista con los repositorios que"\
                            " necesitas* 🗒 para que funcione.\n\nSi quieres contribuir, *no dudes en dejar tu estrella 🌟*,"\
                            " y *compartir el proyecto* 🗣",
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            reply_markup=rp_mk,
                            disable_web_page_preview=True)
        else:
            keyboard = [[InlineKeyboardButton("Go to the project 👁", url=url1),
                         InlineKeyboardButton("Support this bot 🌟", url=url2)]]
            rp_mk = InlineKeyboardMarkup(keyboard)
            bot.sendMessage(chat_id=chat_id,
                            text="_Are you a developer? 🤓 Are you interested in learning? 📚_ *You are in the right place*." \
                                 "\n\nOur policy (_based on Telegram ones_) rely on *OpenSource* project (" 
                                 "free code) 📖 so, this bot is *completely public* 👏\nYou can access to" \
                                 " [GitHub project 🔗](https://github.com/Javinator9889/NewsBot) and see how we did it." \
                                 " It is written in *Python 3* and, in the project, you have a *list with dependencies" \
                                 " you need* 🗒 for working properly.\n\nIf you want to contribute, *don't hesitate to rate 🌟*," \
                                 " and *share the project* 🗣",
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            reply_markup=rp_mk,
                            disable_web_page_preview=True)
