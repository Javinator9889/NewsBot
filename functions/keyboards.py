import telegram
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import functions.database_manager as db_m
import datetime
import pytz


@run_async
def key_del_prog(bot, update, chat_id, lang, message_id):
    act = db_m.get_time_prog(chat_id)
    print(act)
    if act is None:
        if lang == 'es':
            bot.editMessageText(chat_id=chat_id,
                                text="Todavía no tienes programada ninguna hora... Vuelve más tarde",
                                message_id=message_id)
        else:
            bot.editMessageText(chat_id=chat_id,
                                text="You don't have any schedule yet... Comeback later",
                                message_id=message_id)
    else:
        list_act = act.split(",")
        if len(list_act) < 2:
            print("Inside len < 2")
            if lang == 'es':
                print("lang is 'es'")
                text = "Éstas son actualmente las horas que tienes programadas. Pulsa en una para eliminarla"
                del_all = "Eliminar todo"
            else:
                text = "These are actually your scheduled hours. Press on one for deleting it"
                del_all = "Delete all"
            time = str(list_act[0])
            print("Used time:", time)
            time2 = None
        else:
            if lang == 'es':
                text = "Éstas son actualmente las horas que tienes programadas. Pulsa en una para eliminarla"
                del_all = "Eliminar todo"
            else:
                text = "These are actually your scheduled hours. Press on one for deleting it"
                del_all = "Delete all"
            time = str(list_act[0])
            time2 = str(list_act[1])

        if time2 is not None:
            print("time2 is not None")
            keyboard = [[InlineKeyboardButton(time, callback_data='First'), InlineKeyboardButton(time2, callback_data='Second')],
                        [InlineKeyboardButton(del_all, callback_data='All')]]
        else:
            print("time2 is None")
            keyboard = [[InlineKeyboardButton(time, callback_data='First')]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        bot.editMessageText(chat_id=chat_id, text=text, reply_markup=reply_markup, message_id=message_id)


@run_async
def key_time_prog(bot, update, chat_id, lang, message_id):
    if lang == 'es':
        text = "¿Qué quieres actualizar? Elige una opción"
        button_1 = "Programar 🕙"
        button_2 = "Quitar horas 🚫"
    else:
        text = "What you want to do? Choose an option"
        button_1 = "Scheduling 🕙"
        button_2 = "Delete hours🚫"

    keyboard = [[InlineKeyboardButton(button_1, callback_data='add_prog'), InlineKeyboardButton(button_2, callback_data='del_prog')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.editMessageText(chat_id=chat_id, text=text, reply_markup=reply_markup, message_id=message_id)


@run_async
def main_menu(bot, update, chat_id, message_id, lang):
    if lang == 'es':
        pref = "Las preferencias ⚙"
        busq = "Cómo buscar 🔍"
        prog = "Programa alertas 🔔"
        inline = "Modo \"inline\" 🖍"
        basic = "Guía básica 🔖"
        more = "Más..."
    else:
        pref = "The preferences ⚙"
        busq = "How to search 🔍"
        prog = "Setup alerts 🔔"
        inline = "\"Inline\" mode 🖍"
        basic = "Basic guide 🔖"
        more = "More..."

    keyboard = [[InlineKeyboardButton(basic, callback_data='0'), InlineKeyboardButton(pref, callback_data='2')],
                [InlineKeyboardButton(prog, callback_data='4'), InlineKeyboardButton(inline, callback_data='6')],
                [InlineKeyboardButton(busq, callback_data='5'), InlineKeyboardButton(more, callback_data='more_info')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if message_id is None:
        if lang == 'es':
            bot.sendMessage(chat_id=chat_id,
                            text="ɢᴜíᴀ ᴅᴇ ᴜsᴏ" \
                                 "\n\nHola, bienvenido 😃\n\nA continuación *tienes una guía* 📖 para aprender a utilizar este bot:" \
                                 " selecciona 👇 las *diferentes opciones* 🔢 y navega por los distintos *menús que aparecerán*\n\n" \
                                 "❗_Utiliza_ /help _cuando estés haciendo cualquier acción con el bot para obtener ayuda personalizada_",
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            reply_markup=reply_markup)
        elif lang == 'en':
            bot.sendMessage(chat_id=chat_id,
                            text="ᴜsᴀɢᴇ ɢᴜɪᴅᴇ" \
                                 "\n\nHi, welcome 😃\n\nRight now, *you have a guide* 📖 for using this bot:" \
                                 " choose 👇 between *different options* 🔢 and go trough *various menus that will appear*\n\n" \
                                 "❗_Use_ /help _when you are doing something with the bot to get personalized help_",
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            reply_markup=reply_markup)
    else:
        if lang == 'es':
            bot.editMessageText(chat_id=chat_id,
                                text="ɢᴜíᴀ ᴅᴇ ᴜsᴏ" \
                                     "\n\nHola, bienvenido 😃\n\nA continuación *tienes una guía* 📖 para aprender a utilizar este bot:" \
                                     " selecciona 👇 las *diferentes opciones* 🔢 y navega por los distintos *menús que aparecerán*\n\n" \
                                     "❗_Utiliza_ /help _cuando estés haciendo cualquier acción con el bot para obtener ayuda personalizada_",
                                parse_mode=telegram.ParseMode.MARKDOWN,
                                reply_markup=reply_markup,
                                message_id=message_id)
        elif lang == 'en':
            bot.editMessageText(chat_id=chat_id,
                                text="ᴜsᴀɢᴇ ɢᴜɪᴅᴇ" \
                                     "\n\nHi, welcome 😃\n\nRight now, *you have a guide* 📖 for using this bot:" \
                                     " choose 👇 between *different options* 🔢 and go trough *various menus that will appear*\n\n" \
                                     "❗_Use_ /help _when you are doing something with the bot to get personalized help_",
                                parse_mode=telegram.ParseMode.MARKDOWN,
                                reply_markup=reply_markup,
                                message_id=message_id)
    return "OK"


@run_async
def key_tz(bot, update, chat_id):
    lang = db_m.read_lang(chat_id)
    tz = db_m.get_time_diff(chat_id)
    now = datetime.datetime.now(pytz.timezone(tz)).strftime("%H:%M")

    if lang == 'es':
        ys = "Sí 👍"
        no = "No 😰"
    else:
        ys = "Yes 👍"
        no = "No 😰"

    keyboard = [[InlineKeyboardButton(ys, callback_data='yes'), InlineKeyboardButton(no, callback_data='no')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if lang == 'es':
        bot.sendMessage(chat_id=chat_id,
                        text="¿Son las "+now+" dónde vives?",
                        reply_markup=reply_markup)
    else:
        bot.sendMessage(chat_id=chat_id,
                        text="Is "+now+" where you are living?",
                        reply_markup=reply_markup)


@run_async
def key_more(bot, update, chat_id, message_id, lang):
    if lang == 'es':
        apo = "Apoya el proyecto 🌟"
        bck = "⬅ Atrás"
        share = "¡Comparte! 🗣"
        vid = "Ver el vídeo 👁"
        gui = "Guía completa 🔖"
        iq = "share es"
    else:
        apo = "Support the project 🌟"
        bck = "⬅ Back"
        share = "Share! 🗣"
        vid = "Watch video 👁"
        gui = "Complete guide 🔖"
        iq = "share en"
    url = 'https://storebot.me/bot/googlnews_bot'
    yt_url = 'https://youtube.com/'
    gui_url = 'https://wordpress.com'

    keyboard = [[InlineKeyboardButton(apo, url=url), InlineKeyboardButton(vid, url=yt_url)],
                [InlineKeyboardButton(gui, url=gui_url), InlineKeyboardButton(share, switch_inline_query=iq)],
                [InlineKeyboardButton(bck, callback_data='1')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if lang == 'es':
        bot.editMessageText(chat_id=chat_id,
                            text="Muchas gracias por *utilizame* y haber *llegado hasta aquí* 😄 Esta parte es solo para" \
                            " _promocionar este bot_ 🌟: he hecho un *gran esfuerzo* y le he dedicado mucho mucho tiempo" \
                            " para que *uses lo que estás utilizando hoy*.\n\nAquí abajo tienes unos botones donde" \
                            " podrás *puntuar el bot* 🌟, ver 👁 el [video promocional pulsando sobre la miniatura]("+yt_url+")" \
                            ", *compartir el bot 🗣* y acceder a *la guía completa 🔖* en _WordPress_",
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            message_id=message_id,
                            reply_markup=reply_markup)
    else:
        bot.editMessageText(chat_id=chat_id,
                            text="Thank you so much for *using me* and *have come here* 😄 This part is only for" \
                            " _promoting this bot_ 🌟: I did a *big effort*and this bot *took me so much time*" \
                            " in order to you to *use what you are using today*.\n\nRight here, below, you have buttons" \
                            " where you will be able to *rate the bot* 🌟, see 👁 the [promotional video pressing on thumbnail]("+yt_url+")" \
                            ", *share the bot 🗣* and access to the *complete guide 🔖* in _WordPress_",
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            message_id=message_id,
                            reply_markup=reply_markup)


@run_async
def key_guide(bot, update, chat_id, message_id, lang):
    if lang == 'es':
        bck = "⬅ Atrás"
    else:
        bck = "⬅ Back"

    keyboard = [[InlineKeyboardButton(bck, callback_data="1")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if lang == 'es':
        bot.editMessageText(chat_id=chat_id,
                            text="ɢᴜíᴀ ʙásɪᴄᴀ" \
                            "\n\n*1.* Usa /start para recopilar *las últimas noticias* 📈 en base a tus preferencias" \
                            "\n*2.* Envíame palabras clave y *buscaré los mejores resultados* 🌟" \
                            "\n*3.* Configúrame a tu gusto en /preferences, pudiendo incluso *programarme 📆" \
                            " unas horas* para mandarte artículos" \
                            "\n*4.* Revisa las *políticas de privacidad* 👮 en /privacy",
                            message_id=message_id,
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            reply_markup=reply_markup)
    else:
        bot.editMessageText(chat_id=chat_id,
                            text="ʙᴀsɪᴄ ɢᴜɪᴅᴇ" \
                                 "\n\n*1.* Use /start for fetching *latest news* 📈 based on your preferences" \
                                 "\n*2.* Send me *keywords* and I will look for the best results 🌟" \
                                 "\n*3.* Set me up with your *interests* in /preferences, being able also " \
                                 "to set *a schedule* 📆 for sending you articles" \
                                 "\n*4.* Review *privacy policy* 👮 in /privacy",
                            message_id=message_id,
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            reply_markup=reply_markup)


@run_async
def key_lang(bot, update):
    keyboard = [[InlineKeyboardButton("Español 🇪🇸", callback_data='es_1'),
                 InlineKeyboardButton("English 🇬🇧", callback_data='en_1')]]

    reply_markup2 = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(text="Hola, bienvenido 😄. Para poder usar mejor este bot, \
_necesito que me digas tu idioma_\n\nHi, welcome 😄. In order to offer you a better\
 user experience, _I need to know your language_",
                              parse_mode=telegram.ParseMode.MARKDOWN,
                              reply_markup=reply_markup2)

    return "OK"


@run_async
def key_max(bot, update, chat_id, message_id):
    keyboard = [[InlineKeyboardButton("20", callback_data='20')],
                [InlineKeyboardButton("50", callback_data='50')],
                [InlineKeyboardButton("75", callback_data='75')],
                [InlineKeyboardButton("100", callback_data='100')],
                [InlineKeyboardButton("150", callback_data='150')],
                [InlineKeyboardButton("200", callback_data='200')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    lang = db_m.read_lang(chat_id)

    if lang == 'es':
        bot.editMessageText(chat_id=chat_id,
                            text="Selecciona cuántos resultados quieres que aparezcan *como máximo* (por defecto, este valor se establece en _75_ )",
                            message_id=message_id,
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            reply_markup=reply_markup)
    else:
        bot.editMessageText(chat_id=chat_id,
                            text="Choose how many results would you like to be *at most* (by default, this value is _75_ )",
                            message_id=message_id,
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            reply_markup=reply_markup)
    return "OK"


@run_async
def key_two(bot, update, chat_id, lang, message_id):
    if lang == 'es':
        next1 = "Siguiente ➡"
        text = "ᴘʀᴇғᴇʀᴇɴᴄɪᴀs\n\n*Cambia tus preferencias* en /preferences ⚙, añadiendo las que quieras _escribiéndolas una tras otra, separadas por una coma_ \
        \n`(microsoft,España)`.\n\nSi lo que *quieres es eliminarlas* 🗑, sencillamente añade \"Eliminar\" seguido del _número asignado a la preferencia_" \
                "\n\n`1: microsoft\n2: España\n\nEliminar 1,2`\n\nCuando hayas acabado, escribe *Terminado*\n\n`1/2`"
        prev1 = "⬅ Atrás"
    else:
        next1 = "Next ➡"
        text = "ᴘʀᴇғᴇʀᴇɴᴄᴇs\n\n*Change your preferences* ⚙, just adding them _writing one after another, separated by comma_ \
        \n`(microsoft,USA)`.\n\nIf *what you want is deleting them* 🗑, type \"Delete\" followed by the _number of the preference_\
 \n\n`1: microsoft\n2: USA\n\nDelete 1,2`\n\nWhen you have finished, write *Done*\n\n`1/2`"
        prev1 = "⬅ Previously"

    keyboard = [[InlineKeyboardButton(prev1, callback_data="1"), InlineKeyboardButton(next1, callback_data="3")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if message_id is not None:
        bot.editMessageText(chat_id=chat_id,
                            text=text,
                            message_id=message_id,
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            reply_markup=reply_markup)
    else:
        bot.sendMessage(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup)
    return "OK"


@run_async
def key_three(bot, update, chat_id, lang, message_id):
    if lang == 'es':
        nextb = "Menú principal 📋"
        text = "ᴘʀᴇғᴇʀᴇɴᴄɪᴀs\n\n_Prioriza y restringe páginas en tus preferencias:_\
        \n*1. Priorizar*‼: `android ABC`\n*2. Restringir* ⛔: `economía -elpais`\
        \n\n_(el nombre de la página web debe ir todo junto cuando restringes)_\n\n`2/2`"
        prev1 = "⬅ Anterior"
    else:
        nextb = "Main menu 📋"
        text = "ᴘʀᴇғᴇʀᴇɴᴄᴇs\n\n_Prioritize and limit web-pages in your preferences:_\
        \n*1. Prioritize*‼: `windows New York Times`\n*2. Restrict* ⛔: `economy -reuters`\
        \n\n_(web-page must go together while limiting results)_\n\n`2/2`"
        prev1 = "⬅ Previously"
    keyboard = [[InlineKeyboardButton(prev1, callback_data="2"), InlineKeyboardButton(nextb, callback_data="1")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if message_id is not None:
        bot.editMessageText(chat_id=chat_id,
                            text=text,
                            message_id=message_id,
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            reply_markup=reply_markup)
    else:
        bot.sendMessage(chat_id, text, parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup)
    return "OK"


@run_async
def key_four(bot, update, chat_id, lang, message_id):
    if lang == 'es':
        nxt = "Un día a la semana 📆"
        text = "ᴘʀᴏɢʀᴀᴍᴀᴄɪóɴ - ᴛᴏᴅᴏs ʟᴏs ᴅíᴀs\n\nEscribe la *hora y los minutos* para todos los días\n\n`(HH:MM) - (12:15,9:30PM)`"
        prev1 = "⬅ Anterior"
    else:
        nxt = "Once a week 📆"
        text = "sᴄʜᴇᴅᴜʟɪɴɢ - ᴇᴠᴇʀʏ ᴅᴀʏ\n\nWrite the *hour and minutes* for everyday \n\n`(HH:MM) - (12:15,9:30PM)`"
        prev1 = "⬅ Previously"
    keyboard = [[InlineKeyboardButton(prev1, callback_data="1"), InlineKeyboardButton(nxt, callback_data="4_2")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if message_id is not None:
        bot.editMessageText(chat_id=chat_id,
                            text=text,
                            message_id=message_id,
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            reply_markup=reply_markup)
    else:
        bot.sendMessage(chat_id, text, parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup)
    return "OK"


@run_async
def key_four_two(bot, update, chat_id, lang, message_id):
    if lang == 'es':
        prev1 = "⬅ Anterior"
        text = "ᴘʀᴏɢʀᴀᴍᴀᴄɪóɴ - ᴜɴᴀ ᴠᴇᴢ ᴀ ʟᴀ sᴇᴍᴀɴᴀ\n\
        \nEscribe *la hora, los minutos y las tres primeras letras del día* para una vez a la semana 📅\
        \n\n`(HH:MM dom) - (15:40 mar,7:10am jue)`"
        nextb = "Menú principal 📋"
    else:
        nextb = "Main Menu 📋"
        text = "sᴄʜᴇᴅᴜʟɪɴɢ - ᴏɴᴄᴇ ᴀ ᴡᴇᴇᴋ\n\
        \nWrite *hour, minutes and day first three letters* for once a week 📅\
        \n\n`(HH:MM Sun) - (15:40 tue,7:10am thu)`"
        prev1 = "⬅ Previously"

    keyboard = [[InlineKeyboardButton(prev1, callback_data="4"), InlineKeyboardButton(nextb, callback_data='1')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if message_id is not None:
        bot.editMessageText(chat_id=chat_id,
                            text=text,
                            message_id=message_id,
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            reply_markup=reply_markup)
    else:
        bot.sendMessage(chat_id, text, parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup)
    return "OK"


@run_async
def key_five(bot, update, chat_id, lang, message_id):
    if lang == 'es':
        next1 = "Leer más 📰"
        url = "http://pabloaracil.es/trucos-para-buscar-eficientemente-en-google/"
        text = "ɢᴜíᴀ ᴅᴇ ʙúsǫᴜᴇᴅᴀ\n\n*Busca noticias directamente* escribiendo y enviando el _término que quieras buscar._\
        \n*Prioriza páginas o restríngelas* de esta manera:\
\n\n*1. Priorizar*‼: `android ABC`\n*2. Restringir* ⛔: `economía -elpais`\n\nEl bot utiliza el motor de *búsqueda de Google*" \
        ", por lo que puedes leer [aquí](http://pabloaracil.es/trucos-para-buscar-eficientemente-en-google/) algunos *trucos para mejorar tus búsquedas*"
        prev1 = "⬅ Anterior"
    else:
        text = "*5. Look for news directly* writing and sending the _search term._\
        \n*Prioritize or limit web pages* like this:\
\n\n*1. Prioritize*‼: `windows New York Times`\n*2. Restrict* ⛔: `economy -reuters`\n\nThe bot is using *Google search*" \
        ", so you can read [here](http://motto.time.com/4116259/google-search/) some *tricks for improving results*"
        next1 = "Read more 📰"
        url = "http://motto.time.com/4116259/google-search/"
        prev1 = "⬅ Previously"
    keyboard = [[InlineKeyboardButton(prev1, callback_data="1"), InlineKeyboardButton(next1, url=url)]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if message_id is not None:
        bot.editMessageText(chat_id=chat_id,
                            text=text,
                            message_id=message_id,
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            reply_markup=reply_markup,
                            disable_web_page_preview=True)
    else:
        bot.sendMessage(chat_id, text, parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup)
    return "OK"


@run_async
def key_six(bot, update, chat_id, lang, message_id):
    if lang == 'es':
        next1 = "Guía de búsquedas 🔍"
        text = "ᴍᴏᴅᴏ \"ɪɴʟɪɴᴇ\"\n\n*Busca las últimas noticias* 🔎 en cualquier chat escribiendo `@GooglNews_bot es,búsqueda`\
        \n\nLos resultados aparecerán _en una ventana emergente_ donde podrás seleccionar 👇 el que quieras\
        \n\n*Puedes priorizar o limitar resultados* como se explica en el apartado de búsquedas"
        prev1 = "⬅ Anterior"
    else:
        next1 = "Searching guide 🔍"
        text = "\"ɪɴʟɪɴᴇ\" ᴍᴏᴅᴇ\n\n*Fetch for the latest news* 🔎 in every chat typing `@GooglNews_bot en,search-terms`\
        \n\nSearch results will appear in a _pop-up window_ where you will be able to choose 👇 the one you prefer\
        \n\n*You can prioritize or limit results* as explained in searching guide"
        prev1 = "⬅ Previously"
    keyboard = [[InlineKeyboardButton(prev1, callback_data='1'), InlineKeyboardButton(next1, callback_data='5')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if message_id is not None:
        bot.editMessageText(chat_id=chat_id,
                            text=text,
                            message_id=message_id,
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            reply_markup=reply_markup)
    else:
        bot.sendMessage(chat_id, text, parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup)
    return "OK"


@run_async
def key_pref(bot, update, chat_id, message_id):
    lang = db_m.read_lang(chat_id)
    if lang == 'es':
        tec = "Tecnología 💾"
        soc = "Sociedad 👥"
        eco = "Economía 💰"
        inr = "Internacional 🌍"
        dep = "Deporte 🏈"
        cul = "Cultura 🎭"
        done = "Terminado"
    else:
        tec = "Technology 💾"
        soc = "Society 👥"
        eco = "Economy 💰"
        inr = "International 🌍"
        dep = "Sports 🏈"
        cul = "Culture 🎭"
        done = "Done"
    keyboard = [[InlineKeyboardButton(tec, callback_data='tec'), InlineKeyboardButton(soc, callback_data='soc')],
                [InlineKeyboardButton(eco, callback_data='eco'), InlineKeyboardButton(inr, callback_data='inr')],
                [InlineKeyboardButton(dep, callback_data='dep'), InlineKeyboardButton(cul, callback_data='cul')],
                [InlineKeyboardButton(done, callback_data="finished")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if message_id is None:
        if lang == 'es':
            bot.sendMessage(chat_id=chat_id,
                            text="Perfecto 😄\
\nLa configuración inicial está casi. Solo falta que definas algunas preferencias para buscar artículos. Pulsa *\"Terminado\"* cuando hayas acabado",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.sendMessage(chat_id=chat_id,
                            text="Perfect 😄\
\nThe initial setup is already done. Just define some preferences for searching articles. Press on *\"Done\"* when you have finished",
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        if lang == 'es':
            bot.editMessageText(chat_id=chat_id,
                                text="Pulsa en \"Terminado\" para acabar",
                                message_id=message_id,
                                reply_markup=reply_markup)
        else:
            bot.editMessageText(chat_id=chat_id,
                                text="Press on \"Done\" to finish",
                                message_id=message_id,
                                reply_markup=reply_markup)

    return "OK"


@run_async
def key_cul(bot, update, chat_id, message_id):
    lang = db_m.read_lang(chat_id)
    pref = db_m.get_pref(chat_id)
    if lang == 'es':
        if pref is not None and 'música artista' in pref:
            win = "Música ✔"
            cb1 = '6_música artista'
        else:
            win = "Música ❌"
            cb1 = '6_música artista'
        if pref is not None and 'cine estrenos' in pref:
            app = "Cine ✔"
            cb2 = '6_cine estrenos'
        else:
            app = "Cine ❌"
            cb2 = '6_cine estrenos'
        if pref is not None and 'teatro estrenos' in pref:
            anr = "Teatro ✔"
            cb3 = '6_teatro estrenos'
        else:
            anr = "Teatro ❌"
            cb3 = '6_teatro estrenos'
        if pref is not None and 'allintext: "museo" museum' in pref:
            cib = "Museos ✔"
            cb4 = '6_allintext: "museo" museum'
        else:
            cib = "Museos ❌"
            cb4 = '6_allintext: "museo" museum'
        if pref is not None and 'danza musica' in pref:
            viv = "Danza ✔"
            cb5 = '6_danza musica'
        else:
            viv = "Danza ❌"
            cb5 = '6_danza musica'
        back = "⬅ Atrás"
    else:
        if pref is not None and 'music artist' in pref:
            win = "Music ✔"
            cb1 = '6_music artist'
        else:
            win = "Music ❌"
            cb1 = '6_music artist'
        if pref is not None and 'cinema hits' in pref:
            app = "Movies ✔"
            cb2 = '6_cinema hits'
        else:
            app = "Movies ❌"
            cb2 = '6_cinema hits'
        if pref is not None and 'theatre hits' in pref:
            anr = "Theatre ✔"
            cb3 = '6_theatre hits'
        else:
            anr = "Theatre ❌"
            cb3 = '6_theatre hits'
        if pref is not None and 'museum discoveries' in pref:
            cib = "Museums ✔"
            cb4 = '6_museum discoveries'
        else:
            cib = "Museums ❌"
            cb4 = '6_museum discoveries'
        if pref is not None and 'dancing music' in pref:
            viv = "Dancing ✔"
            cb5 = '6_dancing music'
        else:
            viv = "Dancing ❌"
            cb5 = '6_dancing music'
        back = "⬅ Back"

    if lang == 'es':
        keyboard = [[InlineKeyboardButton(win, callback_data=cb1), InlineKeyboardButton(app, callback_data=cb2)],
                    [InlineKeyboardButton(anr, callback_data=cb3), InlineKeyboardButton(cib, callback_data=cb4)],
                    [InlineKeyboardButton(viv, callback_data=cb5), InlineKeyboardButton(back, callback_data="Back")]]
    else:
        keyboard = [[InlineKeyboardButton(win, callback_data=cb1), InlineKeyboardButton(app, callback_data=cb2)],
                    [InlineKeyboardButton(anr, callback_data=cb3), InlineKeyboardButton(cib, callback_data=cb4)],
                    [InlineKeyboardButton(viv, callback_data=cb5), InlineKeyboardButton(back, callback_data="Back")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if lang == 'es':
        bot.editMessageText(chat_id=chat_id, text="Seleccionando las preferencias sobre *Deportes*",
                            message_id=message_id, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        bot.editMessageText(chat_id=chat_id, text="Choosing preferences about *Sports*",
                            message_id=message_id, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)


@run_async
def key_dep(bot, update, chat_id, message_id):
    lang = db_m.read_lang(chat_id)
    pref = db_m.get_pref(chat_id)
    if lang == 'es':
        if pref is not None and 'fútbol' in pref:
            win = "Fútbol ✔"
            cb1 = '5_fútbol'
        else:
            win = "Fútbol ❌"
            cb1 = '5_fútbol'
        if pref is not None and 'baloncesto' in pref:
            app = "Baloncesto ✔"
            cb2 = '5_baloncesto'
        else:
            app = "Baloncesto ❌"
            cb2 = '5_baloncesto'
        if pref is not None and 'ciclismo' in pref:
            anr = "Ciclismo ✔"
            cb3 = '5_ciclismo'
        else:
            anr = "Ciclismo ❌"
            cb3 = '5_ciclismo'
        if pref is not None and 'formula1' in pref:
            cib = "Fórmula 1 ✔"
            cb4 = '5_formula1'
        else:
            cib = "Fórmula 1 ❌"
            cb4 = '5_formula1'
        if pref is not None and 'motogp' in pref:
            viv = "MotoGP ✔"
            cb5 = '5_motogp'
        else:
            viv = "MotoGP ❌"
            cb5 = '5_motogp'
        back = "⬅ Atrás"
    else:
        if pref is not None and 'football' in pref:
            win = "Football ✔"
            cb1 = '5_football'
        else:
            win = "Football ❌"
            cb1 = '5_football'
        if pref is not None and 'basketball' in pref:
            app = "Basketball ✔"
            cb2 = '5_basketball'
        else:
            app = "Basketball ❌"
            cb2 = '5_basketball'
        if pref is not None and 'cycling' in pref:
            anr = "Cycling ✔"
            cb3 = '5_cycling'
        else:
            anr = "Cycling ❌"
            cb3 = '5_cycling'
        if pref is not None and 'formula1' in pref:
            cib = "Formula 1 ✔"
            cb4 = '5_formula1'
        else:
            cib = "Formula 1 ❌"
            cb4 = '5_formula1'
        if pref is not None and 'motogp' in pref:
            viv = "MotoGP ✔"
            cb5 = '5_motogp'
        else:
            viv = "MotoGP ❌"
            cb5 = '5_motogp'
        back = "⬅ Back"

    if lang == 'es':
        keyboard = [[InlineKeyboardButton(win, callback_data=cb1), InlineKeyboardButton(app, callback_data=cb2)],
                    [InlineKeyboardButton(anr, callback_data=cb3), InlineKeyboardButton(cib, callback_data=cb4)],
                    [InlineKeyboardButton(viv, callback_data=cb5), InlineKeyboardButton(back, callback_data="Back")]]
    else:
        keyboard = [[InlineKeyboardButton(win, callback_data=cb1), InlineKeyboardButton(app, callback_data=cb2)],
                    [InlineKeyboardButton(anr, callback_data=cb3), InlineKeyboardButton(cib, callback_data=cb4)],
                    [InlineKeyboardButton(viv, callback_data=cb5), InlineKeyboardButton(back, callback_data="Back")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if lang == 'es':
        bot.editMessageText(chat_id=chat_id, text="Seleccionando las preferencias sobre *Deportes*",
                            message_id=message_id, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        bot.editMessageText(chat_id=chat_id, text="Choosing preferences about *Sports*",
                            message_id=message_id, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)


@run_async
def key_int(bot, update, chat_id, message_id):
    lang = db_m.read_lang(chat_id)
    pref = db_m.get_pref(chat_id)
    if lang == 'es':
        if pref is not None and 'noticias' in pref:
            win = "Noticias generales ✔"
            cb1 = '4_noticias'
        else:
            win = "Noticias generales ❌"
            cb1 = '4_noticias'
        if pref is not None and 'UE union europea' in pref:
            app = "Unión Europea ✔"
            cb2 = '4_UE union europea'
        else:
            app = "Unión Europea ❌"
            cb2 = '4_UE union europea'
        if pref is not None and 'america noticias news' in pref:
            anr = "América ✔"
            cb3 = '4_america noticias news'
        else:
            anr = "América ❌"
            cb3 = '4_america noticias news'
        if pref is not None and 'noticias asia' in pref:
            cib = "Asia ✔"
            cb4 = '4_noticias asia'
        else:
            cib = "Asia ❌"
            cb4 = '4_noticias asia'
        back = "⬅ Atrás"
    else:
        if pref is not None and 'international news' in pref:
            win = "General News ✔"
            cb1 = '4_international news'
        else:
            win = "General News ❌"
            cb1 = '4_international news'
        if pref is not None and 'european union' in pref:
            app = "European Union ✔"
            cb2 = '4_european union'
        else:
            app = "European Union ❌"
            cb2 = '4_european union'
        if pref is not None and 'news america' in pref:
            anr = "America ✔"
            cb3 = '4_news america'
        else:
            anr = "America ❌"
            cb3 = '4_news america'
        if pref is not None and 'noticias asia' in pref:
            cib = "Asia ✔"
            cb4 = '4_news asia'
        else:
            cib = "Asia ❌"
            cb4 = '4_news asia'
        back = "⬅ Back"

    keyboard = [[InlineKeyboardButton(win, callback_data=cb1), InlineKeyboardButton(app, callback_data=cb2)],
                [InlineKeyboardButton(anr, callback_data=cb3), InlineKeyboardButton(cib, callback_data=cb4)],
                [InlineKeyboardButton(back, callback_data="Back")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if lang == 'es':
        bot.editMessageText(chat_id=chat_id, text="Seleccionando las preferencias sobre *Internacional*",
                            message_id=message_id, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        bot.editMessageText(chat_id=chat_id, text="Choosing preferences about *Internacional*",
                            message_id=message_id, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)


@run_async
def key_eco(bot, update, chat_id, message_id):
    lang = db_m.read_lang(chat_id)
    pref = db_m.get_pref(chat_id)
    if lang == 'es':
        if pref is not None and 'bancos economía' in pref:
            win = "Macroeconomía ✔"
            cb1 = '3_bancos economía'
        else:
            win = "Macroeconomía ❌"
            cb1 = '3_bancos economía'
        if pref is not None and 'empresas compañías economía' in pref:
            app = "Empresas ✔"
            cb2 = '3_empresas compañías economía'
        else:
            app = "Empresas ❌"
            cb2 = '3_empresas compañías economía'
        if pref is not None and 'turismo economía' in pref:
            anr = "Turismo ✔"
            cb3 = '3_turismo economía'
        else:
            anr = "Turismo ❌"
            cb3 = '3_turismo economía'
        if pref is not None and 'bolsa economía' in pref:
            cib = "Bolsa ✔"
            cb4 = '3_bolsa economía'
        else:
            cib = "Bolsa ❌"
            cb4 = '3_bolsa economía'
        if pref is not None and 'vivienda economía' in pref:
            viv = "Vivienda ✔"
            cb5 = '3_vivienda economía'
        else:
            viv = "Vivienda ❌"
            cb5 = '3_vivienda economía'
        back = "⬅ Atrás"
    else:
        if pref is not None and 'economy banks' in pref:
            win = "Macroeconomy ✔"
            cb1 = '3_economy banks'
        else:
            win = "Macroeconomy ❌"
            cb1 = '3_economy banks'
        if pref is not None and 'corporations economy' in pref:
            app = "Enterprises ✔"
            cb2 = '3_corporations economy'
        else:
            app = "Enterprises ❌"
            cb2 = '3_corporations economy'
        if pref is not None and 'turism economy' in pref:
            anr = "Turism ✔"
            cb3 = '3_turism economy'
        else:
            anr = "Turism ❌"
            cb3 = '3_turism economy'
        if pref is not None and 'stock exchange economy' in pref:
            cib = "Stock Exchange ✔"
            cb4 = '3_stock exchange economy'
        else:
            cib = "Stock Exchange ❌"
            cb4 = '3_stock exchange economy'
        if pref is not None and 'housing economy' in pref:
            viv = "Housing ✔"
            cb5 = '3_housing economy'
        else:
            viv = "Housing ❌"
            cb5 = '3_housing economy'
        back = "⬅ Back"

    if lang == 'es':
        keyboard = [[InlineKeyboardButton(win, callback_data=cb1), InlineKeyboardButton(app, callback_data=cb2)],
                    [InlineKeyboardButton(anr, callback_data=cb3), InlineKeyboardButton(cib, callback_data=cb4)],
                    [InlineKeyboardButton(viv, callback_data=cb5), InlineKeyboardButton(back, callback_data="Back")]]
    else:
        keyboard = [[InlineKeyboardButton(win, callback_data=cb1), InlineKeyboardButton(app, callback_data=cb2)],
                    [InlineKeyboardButton(anr, callback_data=cb3), InlineKeyboardButton(cib, callback_data=cb4)],
                    [InlineKeyboardButton(viv, callback_data=cb5), InlineKeyboardButton(back, callback_data="Back")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if lang == 'es':
        bot.editMessageText(chat_id=chat_id, text="Seleccionando las preferencias sobre *Economía*",
                            message_id=message_id, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        bot.editMessageText(chat_id=chat_id, text="Choosing preferences about *Economy*",
                            message_id=message_id, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)


@run_async
def key_soc(bot, update, chat_id, message_id):
    lang = db_m.read_lang(chat_id)
    pref = db_m.get_pref(chat_id)
    if lang == 'en':
        if pref is not None and 'health discoveries' in pref:
            win = "Health ✔"
            cb1 = '2_health discoveries'
        else:
            win = "Health ❌"
            cb1 = '2_health discoveries'
        if pref is not None and 'allintext: "america"' in pref:
            app = "America ✔"
            cb2 = '2_allintext: "america"'
        else:
            app = "America ❌"
            cb2 = '2_allintext: "america"'
        if pref is not None and 'law global' in pref:
            anr = "Law ✔"
            cb3 = '2_law global'
        else:
            anr = "Law ❌"
            cb3 = '2_law global'
        if pref is not None and 'job contract' in pref:
            cib = "Jobs ✔"
            cb4 = '2_job contract'
        else:
            cib = "Jobs ❌"
            cb4 = '2_job contract'
        back = "⬅ Back"
    else:
        if pref is not None and 'salud españa' in pref:
            win = "Salud ✔"
            cb1 = '2_salud españa'
        else:
            win = "Salud ❌"
            cb1 = '2_salud españa'
        if pref is not None and 'allintext: "españa"' in pref:
            app = "España ✔"
            cb2 = '2_allintext: "españa"'
        else:
            app = "España ❌"
            cb2 = '2_allintext: "españa"'
        if pref is not None and 'leyes españa' in pref:
            anr = "Legislación ✔"
            cb3 = '2_leyes españa'
        else:
            anr = "Legislación ❌"
            cb3 = '2_leyes españa'
        if pref is not None and 'oposiciones españa' in pref:
            cib = "Oposiciones ✔"
            cb4 = '2_oposiciones españa'
        else:
            cib = "Oposiciones ❌"
            cb4 = '2_oposiciones españa'
        if pref is not None and 'empleo españa' in pref:
            goo = "Trabajo ✔"
            cb5 = '2_empleo españa'
        else:
            goo = "Trabajo ❌"
            cb5 = '2_empleo españa'
        back = "⬅ Atrás"

    if lang == 'es':
        keyboard = [[InlineKeyboardButton(win, callback_data=cb1), InlineKeyboardButton(app, callback_data=cb2)],
                    [InlineKeyboardButton(anr, callback_data=cb3), InlineKeyboardButton(cib, callback_data=cb4)],
                    [InlineKeyboardButton(goo, callback_data=cb5), InlineKeyboardButton(back, callback_data="Back")]]
    else:
        keyboard = [[InlineKeyboardButton(win, callback_data=cb1), InlineKeyboardButton(app, callback_data=cb2)],
                    [InlineKeyboardButton(anr, callback_data=cb3), InlineKeyboardButton(cib, callback_data=cb4)],
                    [InlineKeyboardButton(back, callback_data="Back")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if lang == 'es':
        bot.editMessageText(chat_id=chat_id, text="Seleccionando las preferencias sobre *Sociedad*",
                            message_id=message_id, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        bot.editMessageText(chat_id=chat_id, text="Choosing preferences about *Society*",
                            message_id=message_id, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)


@run_async
def key_tec(bot, update, chat_id, message_id):
    lang = db_m.read_lang(chat_id)
    pref = db_m.get_pref(chat_id)
    if lang == 'es':
        if pref is not None and 'windows' in pref:
            win = "Windows ✔"
            cb1 = "1_windows"
        else:
            win = "Windows ❌"
            cb1 = "1_windows"
        if pref is not None and 'apple' in pref:
            app = "Apple ✔"
            cb2 = "1_apple"
        else:
            app = "Apple ❌"
            cb2 = "1_apple"
        if pref is not None and 'android -juegos' in pref:
            anr = "Android ✔"
            cb3 = "1_android -juegos"
        else:
            anr = "Android ❌"
            cb3 = "1_android -juegos"
        if pref is not None and 'ciberseguridad' in pref:
            cib = "Ciberseguridad ✔"
            cb4 = "1_ciberseguridad"
        else:
            cib = "Ciberseguridad ❌"
            cb4 = "1_ciberseguridad"
        if pref is not None and 'google' in pref:
            goo = "Google ✔"
            cb5 = "1_google"
        else:
            goo = "Google ❌"
            cb5 = "1_google"
        if pref is not None and 'nueva tecnología' in pref:
            nt = "Invenciones ✔"
            cb6 = "1_nueva tecnología"
        else:
            nt = "Invenciones ❌"
            cb6 = "1_nueva tecnología"
        back = "⬅ Atrás"
    else:
        if pref is not None and 'windows' in pref:
            win = "Windows ✔"
            cb1 = "1_windows"
        else:
            win = "Windows ❌"
            cb1 = "1_windows"
        if pref is not None and 'apple ios mac phone' in pref:
            app = "Apple ✔"
            cb2 = "1_apple ios mac phone"
        else:
            app = "Apple ❌"
            cb2 = "1_apple ios mac phone"
        if pref is not None and 'android -games' in pref:
            anr = "Android ✔"
            cb3 = "1_android -games"
        else:
            anr = "Android ❌"
            cb3 = "1_android -games"
        if pref is not None and 'cybersecurity' in pref:
            cib = "Cybersecurity ✔"
            cb4 = "1_cybersecurity"
        else:
            cib = "Cybersecurity ❌"
            cb4 = '1_cybersecurity'
        if pref is not None and 'google' in pref:
            goo = "Google ✔"
            cb5 = "1_google"
        else:
            goo = "Google ❌"
            cb5 = "1_google"
        if pref is not None and 'new technology inventions' in pref:
            nt = "Inventions ✔"
            cb6 = "1_new technology inventions"
        else:
            nt = "Inventions ❌"
            cb6 = "1_new technology inventions"
        back = "⬅ Back"

    keyboard = [[InlineKeyboardButton(win, callback_data=cb1), InlineKeyboardButton(app, callback_data=cb2)],
                [InlineKeyboardButton(anr, callback_data=cb3), InlineKeyboardButton(cib, callback_data=cb4)],
                [InlineKeyboardButton(goo, callback_data=cb5), InlineKeyboardButton(nt, callback_data=cb6)],
                [InlineKeyboardButton(back, callback_data="Back")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if lang == 'es':
        bot.editMessageText(chat_id=chat_id, text="Seleccionando las preferencias sobre *Tecnología*",
                            message_id=message_id, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        bot.editMessageText(chat_id=chat_id, text="Choosing preferences about *Technology*",
                            message_id=message_id, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)
