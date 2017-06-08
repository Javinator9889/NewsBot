from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from functions.news_keyboard_results import key_var
import functions.database_manager as db_m
import functions.start_handler as started
import functions.help as hp
from functions.keyboards import *
import functions.start_handler as st
import functions.botan as botan
import os
import os.path as path
import re
import datetime


@run_async
def key_lang(bot, update, chat_id, message_id):
    keyboard = [[InlineKeyboardButton("Español 🇪🇸", callback_data='es'),
                 InlineKeyboardButton("English 🇬🇧", callback_data='en')]]

    reply_markup2 = InlineKeyboardMarkup(keyboard)

    bot.editMessageText(chat_id=chat_id,
                        text='Elige tu idioma / choose your language:',
                        message_id=message_id,
                        parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup2)
    return "OK"


@run_async
def key_prefes(bot, update, chat_id, message_id, lang):
    if lang == 'es':
        change = "Editar las preferencias"
        bck = "◀ Volver atrás"
    else:
        change = "Edit preferences"
        bck = "◀ Go back"

    keyboard = [[InlineKeyboardButton(change, callback_data='pref'), InlineKeyboardButton(bck, callback_data='pref2')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    actual_pref = db_m.get_pref(chat_id)
    if actual_pref == '' or actual_pref is None:
        act_list = []
    else:
        act_list = actual_pref.split(",")
    if len(act_list) == 0:
        if lang == 'es':
            comp_list = "_vacío_"
        else:
            comp_list = "_empty_"
    else:
        for a in range(0, len(act_list) - 1):
            lst = re.findall(r'"(.*?)(?<!\\)"', act_list[a])
            if a == 0:
                try:
                    comp_list = "*" + str(a + 1) + "*: " + "_" + lst[0] + "_" + "\n"
                except IndexError:
                    comp_list = "*" + str(a + 1) + "*: " + "_" + act_list[a] + "_" + "\n"
            else:
                if act_list[a] != '':
                    try:
                        comp_list += "*" + str(a + 1) + "*: " + "_" + lst[0] + "_" + "\n"
                    except IndexError:
                        comp_list += "*" + str(a + 1) + "*: " + "_" + act_list[a] + "_" + "\n"
    if lang == 'es':
        bot.editMessageText(chat_id=chat_id,
                            text="Tus *preferencias actualmente* son las siguientes:\n" + comp_list + "",
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            message_id=message_id,
                            reply_markup=reply_markup)
    else:
        bot.editMessageText(chat_id=chat_id,
                            text="Your *actual preferences* are the following ones:\n" + comp_list + "",
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            message_id=message_id,
                            reply_markup=reply_markup)


@run_async
def callb_button(bot, update):
    query = update.callback_query
    chat_id = query['message']['chat']['id']
    update.callback_query.answer()
    value = query.data
    msg_id = query.message.message_id
    get_chat_id = db_m.read_chatid(chat_id)
    if get_chat_id is None:
        bot.sendMessage(chat_id,
                        text="*Disculpa las molestias*, pero tienes que _volver a configurar el bot_. Escribe /start o púlsalo" \
                             "\n\n*We are sorry*, but you have to _configure again the bot_. Type /start or press on it",
                        parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        db_m.last_usage(chat_id, datetime.datetime.now().strftime("%H:%M %d-%m-%Y"))
        lang = db_m.read_lang(chat_id)
        print("\n\tSelected option:", value)
        if value == 'next1':
            key_var(bot, update, chat_id, msg_id, True)
        elif value == 'next':
            key_var(bot, update, chat_id, msg_id, True)
        elif value == 'prev':
            key_var(bot, update, chat_id, msg_id, False)
        elif value == 'es':
            db_m.write_lang(chat_id, value)
            bot.editMessageText(chat_id=chat_id, text="Preferencias actualizadas correctamente. Cámbialas cuando quieras \
    en /config",
                                message_id=msg_id)
        elif value == 'en':
            db_m.write_lang(chat_id, value)
            bot.editMessageText(chat_id=chat_id,
                                text="Preferences updated correctly. Change them in /config",
                                message_id=msg_id)
        elif value == 'yes':
            if db_m.is_time(chat_id, None) == '1':
                if path.exists("first_run_{}".format(chat_id)):
                    bot.deleteMessage(chat_id=chat_id, message_id=msg_id)
                    db_m.is_time(chat_id, False)
                    st.cont_2(bot, update, chat_id)
                elif lang == 'es':
                    bot.editMessageText(chat_id=chat_id,
                                        text="Perfecto, hemos actualizado tu *zona horaria* 🌍",
                                        message_id=msg_id,
                                        parse_mode=telegram.ParseMode.MARKDOWN)
                else:
                    bot.editMessageText(chat_id=chat_id,
                                        text="Perfect, we have just updated your *time-zone* 🌍",
                                        message_id=msg_id,
                                        parse_mode=telegram.ParseMode.MARKDOWN)
                db_m.is_time(chat_id, False)
        elif value == 'no':
            if db_m.is_time(chat_id, None) == '1':
                if lang == 'es':
                    bot.editMessageText(chat_id=chat_id,
                                        text="Prueba a enviar tu *ciudad y país* 🌍 o también puedes *enviar tu ubicación* 🛰",
                                        message_id=msg_id,
                                        parse_mode=telegram.ParseMode.MARKDOWN)
                else:
                    bot.editMessageText(chat_id=chat_id,
                                        text="Try to send your *city and country* 🌍 or also you can send *your location* 🛰",
                                        message_id=msg_id,
                                        parse_mode=telegram.ParseMode.MARKDOWN)
        elif value == "tec":
            key_tec(bot, update, chat_id, msg_id)
        elif value == "soc":
            key_soc(bot, update, chat_id, msg_id)
        elif value == "eco":
            key_eco(bot, update, chat_id, msg_id)
        elif value == "inr":
            key_int(bot, update, chat_id, msg_id)
        elif value == "dep":
            key_dep(bot, update, chat_id, msg_id)
        elif value == "cul":
            key_cul(bot, update, chat_id, msg_id)
        elif value == "finished":
            db_m.is_pref(chat_id, False)
            if lang == 'es':
                bot.editMessageText(chat_id=chat_id,
                                    text="Genial 😄 Ya está todo configurado. Ahora puedes:"\
                                    "\n■ Escribir /start para *empezar a recopilar noticias*" \
                                    "\n■ Usar /help para acceder a la *guía de uso*" \
                                    "\n■ Editar *tus preferencias* en /config" \
                                    "\n\n*NOTA:* accede al _menú_ pulsando la barra  *[ / ]*  que aparece _abajo a la derecha_",
                                    message_id=msg_id,
                                    parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.editMessageText(chat_id=chat_id,
                                    text="It's all configured 😄 Now you can:"\
                                    "\n■ Write /start for *fetching the latest news*"\
                                    "\n■ Use /help for going to the *usage guide*"\
                                    "\n■ Edit *your preferences* in /config" \
                                    "\n\n*INFO:* access to the _menu_ using the slash  *[ / ]*  that is at the _bottom right_",
                                    message_id=msg_id,
                                    parse_mode=telegram.ParseMode.MARKDOWN)
            os.remove("first_run_{}".format(chat_id))
        elif value == 'es_1':
            db_m.write_lang(chat_id, "es")
            started.cont_1(bot, update, chat_id, msg_id)
        elif value == 'en_1':
            db_m.write_lang(chat_id, "en")
            started.cont_1(bot, update, chat_id, msg_id)
        elif value == '0':
            key_guide(bot, update, chat_id, msg_id, lang)
        elif value == '1':
            main_menu(bot, update, chat_id, msg_id, lang)
        elif value == '2':
            key_two(bot, update, chat_id, lang, msg_id)
        elif value == '3':
            key_three(bot, update, chat_id, lang, msg_id)
        elif value == '4':
            key_four(bot, update, chat_id, lang, msg_id)
        elif value == '4_2':
            key_four_two(bot, update, chat_id, lang, msg_id)
        elif value == '5':
            key_five(bot, update, chat_id, lang, msg_id)
        elif value == '6':
            key_six(bot, update, chat_id, lang, msg_id)
        elif value == 'more_info':
            key_more(bot, update, chat_id, msg_id, lang)
        elif value == 'tz':
            if lang == 'es':
                bot.editMessageText(chat_id=chat_id,
                                    text="¿Dónde vives? También puedes mandarme *tu ubicación* 🛰",
                                    parse_mode=telegram.ParseMode.MARKDOWN,
                                    message_id=msg_id)
            else:
                bot.editMessageText(chat_id=chat_id,
                                    text="Where are you living? Also, you can send *your location* 🛰",
                                    parse_mode=telegram.ParseMode.MARKDOWN,
                                    message_id=msg_id)
            db_m.is_time(chat_id, True)
        elif value == 'lang':
            key_lang(bot, update, chat_id, msg_id)
        elif value == 'pref':
            actual_pref = db_m.get_pref(chat_id)
            if actual_pref == '' or actual_pref is None:
                act_list = []
            else:
                act_list = actual_pref.split(",")
            if len(act_list) == 0:
                if lang == 'es':
                    comp_list = "_vacío_"
                else:
                    comp_list = "_empty_"
            else:
                for a in range(0, len(act_list)-1):
                    lst = re.findall(r'"(.*?)(?<!\\)"', act_list[a])
                    if a == 0:
                        try:
                            comp_list = "*" + str(a+1) + "*: " + "_" + lst[0] + "_" + "\n"
                        except IndexError:
                            comp_list = "*" + str(a+1) + "*: " + "_" + act_list[a] + "_" + "\n"
                    else:
                        if act_list[a] != '':
                            try:
                                comp_list += "*" + str(a + 1) + "*: " + "_" + lst[0] + "_" + "\n"
                            except IndexError:
                                comp_list += "*" + str(a + 1) + "*: " + "_" + act_list[a] + "_" + "\n"
            if lang == 'es':
                bot.editMessageText(chat_id=chat_id,
                                    text="Tus *preferencias actualmente* son las siguientes:\n"+comp_list+"",
                                    parse_mode=telegram.ParseMode.MARKDOWN,
                                    message_id=msg_id)
                bot.sendMessage(chat_id=chat_id,
                                text="*1.* Añade tus preferencias separándolas *por una coma* \
                                \n`bolsa,fuegos artificiales` \
                                \n*2.* 🗑 Elimínalas escribiendo *Eliminar seguid del número de la preferencia*\
                                \n`Eliminar 1,2`\n\
                                \nEscribe *Terminado* cuando hayas acabado o\
                                \n*Cancelar* dejarlo todo como estaba (si usas /help podrás ver la ayuda para este apartado)",
                                parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.editMessageText(chat_id=chat_id,
                                    text="Your *actual preferences* are the following ones:\n" + comp_list + "",
                                    parse_mode=telegram.ParseMode.MARKDOWN,
                                    message_id=msg_id)
                bot.sendMessage(chat_id=chat_id,
                                text="*1.* Add your preferences *splitting them with a comma*\
                                \n`economy, New York weather` \
                                \n*2.* 🗑 Delete one typing *Delete followed by preference number*\
                                \n`Delete 1,2`\n\
                                \nWrite *Done* when you have finished or\
                                \n*Cancel* for doing no changes(in /help you will get personalized help for this)",
                                parse_mode=telegram.ParseMode.MARKDOWN)
            db_m.is_pref(chat_id, True)
        elif value == 'lista':
            key_prefes(bot, update, chat_id, msg_id, lang)
        elif value == 'pref2':
            key_pref2(bot, update, chat_id, msg_id)
        elif value == 'prog':
            key_time_prog(bot, update, chat_id, lang, msg_id)
        elif value == 'First':
            act = db_m.get_time_prog(chat_id)
            real = db_m.read_prog(chat_id)
            l_act = act.split(",")
            l_real = real.split(",")
            out_1 = [var for var in l_act if var]
            out_2 = [var for var in l_real if var]
            val_1 = out_1[0]
            val_2 = out_2[0]
            out_1.remove(val_1)
            out_2.remove(val_2)
            final = [var for var in out_1 if var]
            final_2 = [var for var in out_2 if var]
            if not final:
                final = None
            else:
                final = final[0]
            if not final_2:
                final_2 = None
            else:
                final_2 = final_2[0]
            db_m.update_prog(chat_id, final)
            db_m.update_prog_time(final_2, chat_id)
            if lang == 'es':
                bot.editMessageText(chat_id=chat_id, text="Listo ✔ Se *ha borrado* la hora", message_id=msg_id, parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.editMessageText(chat_id=chat_id, text="Done ✔ Chosen *time was deleted*", message_id=msg_id, parse_mode=telegram.ParseMode.MARKDOWN)
        elif value == 'Second':
            act = db_m.get_time_prog(chat_id)
            real = db_m.read_prog(chat_id)
            l_act = act.split(",")
            l_real = real.split(",")
            out_1 = [var for var in l_act if var]
            out_2 = [var for var in l_real if var]
            val_1 = out_1[1]
            val_2 = out_2[1]
            out_1.remove(val_1)
            out_2.remove(val_2)
            final = [var for var in out_1 if var]
            final_2 = [var for var in out_2 if var]
            db_m.update_prog(chat_id, final[0])
            db_m.update_prog_time(final_2[0], chat_id)
            if lang == 'es':
                bot.editMessageText(chat_id=chat_id, text="Listo ✔ Se *ha borrado* la hora", message_id=msg_id, parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.editMessageText(chat_id=chat_id, text="Done ✔ Chosen *time was deleted*", message_id=msg_id, parse_mode=telegram.ParseMode.MARKDOWN)
        elif value == 'All':
            db_m.update_prog(chat_id, None)
            db_m.update_prog_time(None, chat_id)
            if lang == 'es':
                bot.editMessageText(chat_id=chat_id, text="Listo ✔ Se *han borrado* las horas", message_id=msg_id, parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.editMessageText(chat_id=chat_id, text="Done ✔ Chosen *time was deleted*", message_id=msg_id, parse_mode=telegram.ParseMode.MARKDOWN)
        elif value == 'add_prog':
            if lang == 'es':
                bot.editMessageText(chat_id=chat_id,
                                    text="Manda las horas *que quieras programar* con el siguiente formato:\
                \n\n`HH:MM` ó `HH:MM lun`. *Escribe* /help *para obtener más información*",
                                    parse_mode=telegram.ParseMode.MARKDOWN,
                                    message_id=msg_id)
            else:
                bot.editMessageText(chat_id=chat_id,
                                    text="Send the *scheduling time* in this format:\
                            \n\n`HH:MM` or `HH:MM Mon`. *Type* /help *for getting help*",
                                    parse_mode=telegram.ParseMode.MARKDOWN,
                                    message_id=msg_id)
            db_m.is_prog(chat_id, True)
        elif value == 'del_prog':
            key_del_prog(bot, update, chat_id, lang, msg_id)
        elif value == 'max':
            key_max(bot, update, chat_id, msg_id)
        elif value == 'es':
            db_m.write_lang(chat_id, value)
            bot.editMessageText(chat_id=chat_id,
                                text="Preferencias de idioma _actualizadas correctamente_",
                                message_id=msg_id,
                                parse_mode=telegram.ParseMode.MARKDOWN)
        elif value == 'en':
            db_m.write_lang(chat_id, value)
            bot.editMessageText(chat_id=chat_id,
                                text="Language preferences _updated correctly_",
                                message_id=msg_id,
                                parse_mode=telegram.ParseMode.MARKDOWN)
        elif value == "Back":
            key_pref(bot, update, chat_id, msg_id)
        elif value == "20":
            db_m.update_max(int(value), chat_id)
            if lang == 'es':
                bot.editMessageText(chat_id=chat_id,
                                    text="Listo. Ahora _recibirás como máximo 20 resultados_ 😄",
                                    message_id=msg_id,
                                    parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.editMessageText(chat_id=chat_id,
                                    text="Done. Now you _will receive at most 20 results_ 😄",
                                    message_id=msg_id,
                                    parse_mode=telegram.ParseMode.MARKDOWN)
        elif value == "50":
            db_m.update_max(int(value), chat_id)
            if lang == 'es':
                bot.editMessageText(chat_id=chat_id,
                                    text="Listo. Ahora _recibirás como máximo 50 resultados_ 😄",
                                    message_id=msg_id,
                                    parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.editMessageText(chat_id=chat_id,
                                    text="Done. Now you _will receive at most 50 results_ 😄",
                                    message_id=msg_id,
                                    parse_mode=telegram.ParseMode.MARKDOWN)
        elif value == "75":
            db_m.update_max(int(value), chat_id)
            if lang == 'es':
                bot.editMessageText(chat_id=chat_id,
                                    text="Listo. Ahora _recibirás como máximo 75 resultados_ 😄",
                                    message_id=msg_id,
                                    parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.editMessageText(chat_id=chat_id,
                                    text="Done. Now you _will receive at most 75 results_ 😄",
                                    message_id=msg_id,
                                    parse_mode=telegram.ParseMode.MARKDOWN)
        elif value == "100":
            db_m.update_max(int(value), chat_id)
            if lang == 'es':
                bot.editMessageText(chat_id=chat_id,
                                    text="Listo. Ahora _recibirás como máximo 100 resultados_ 😄",
                                    message_id=msg_id,
                                    parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.editMessageText(chat_id=chat_id,
                                    text="Done. Now you _will receive at most 100 results_ 😄",
                                    message_id=msg_id,
                                    parse_mode=telegram.ParseMode.MARKDOWN)
        elif value == "150":
            db_m.update_max(int(value), chat_id)
            if lang == 'es':
                bot.editMessageText(chat_id=chat_id,
                                    text="Listo. Ahora _recibirás como máximo 150 resultados_ 😄",
                                    message_id=msg_id,
                                    parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.editMessageText(chat_id=chat_id,
                                    text="Done. Now you _will receive at most 150 results_ 😄",
                                    message_id=msg_id,
                                    parse_mode=telegram.ParseMode.MARKDOWN)
        elif value == "200":
            db_m.update_max(int(value), chat_id)
            if lang == 'es':
                bot.editMessageText(chat_id=chat_id,
                                    text="Listo. Ahora _recibirás como máximo 200 resultados_ 😄",
                                    message_id=msg_id,
                                    parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.editMessageText(chat_id=chat_id,
                                    text="Done. Now you _will receive at most 200 results_ 😄",
                                    message_id=msg_id,
                                    parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            preferences = db_m.get_pref(chat_id)
            if '1_' in value:
                if preferences is None:
                    updated_pref = value[2:] + ","
                    db_m.update_pref(chat_id, updated_pref)
                elif value[2:] in preferences:
                    updated_pref = preferences.replace(value[2:] + ",", "")
                    db_m.update_pref(chat_id, updated_pref)
                else:
                    updated_pref = preferences + value[2:] + ","
                    db_m.update_pref(chat_id, updated_pref)
                key_tec(bot, update, chat_id, msg_id)
            elif '2_' in value:
                if preferences is None:
                    updated_pref = value[2:] + ","
                    db_m.update_pref(chat_id, updated_pref)
                elif value[2:] in preferences:
                    updated_pref = preferences.replace(value[2:] + ",", "")
                    db_m.update_pref(chat_id, updated_pref)
                else:
                    updated_pref = preferences + value[2:] + ","
                    db_m.update_pref(chat_id, updated_pref)
                key_soc(bot, update, chat_id, msg_id)
            elif '3_' in value:
                if preferences is None:
                    updated_pref = value[2:] + ","
                    db_m.update_pref(chat_id, updated_pref)
                elif value[2:] in preferences:
                    updated_pref = preferences.replace(value[2:] + ",", "")
                    db_m.update_pref(chat_id, updated_pref)
                else:
                    updated_pref = preferences + value[2:] + ","
                    db_m.update_pref(chat_id, updated_pref)
                key_eco(bot, update, chat_id, msg_id)
            elif '4_' in value:
                if preferences is None:
                    updated_pref = value[2:] + ","
                    db_m.update_pref(chat_id, updated_pref)
                elif value[2:] in preferences:
                    updated_pref = preferences.replace(value[2:] + ",", "")
                    db_m.update_pref(chat_id, updated_pref)
                else:
                    updated_pref = preferences + value[2:] + ","
                    db_m.update_pref(chat_id, updated_pref)
                key_int(bot, update, chat_id, msg_id)
            elif '5_' in value:
                if preferences is None:
                    updated_pref = value[2:] + ","
                    db_m.update_pref(chat_id, updated_pref)
                elif value[2:] in preferences:
                    updated_pref = preferences.replace(value[2:] + ",", "")
                    db_m.update_pref(chat_id, updated_pref)
                else:
                    updated_pref = preferences + value[2:] + ","
                    db_m.update_pref(chat_id, updated_pref)
                key_dep(bot, update, chat_id, msg_id)
            elif '6_' in value:
                if preferences is None:
                    updated_pref = value[2:] + ","
                    db_m.update_pref(chat_id, updated_pref)
                elif value[2:] in preferences:
                    updated_pref = preferences.replace(value[2:] + ",", "")
                    db_m.update_pref(chat_id, updated_pref)
                else:
                    updated_pref = preferences + value[2:] + ","
                    db_m.update_pref(chat_id, updated_pref)
                key_cul(bot, update, chat_id, msg_id)
