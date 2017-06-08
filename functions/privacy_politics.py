import functions.database_manager as db_m
import os.path as path
import datetime
import telegram


def policy(bot, update):
    chat_id = update.message.chat_id
    print("Executing /privacy")
    get_chat_id = db_m.read_chatid(chat_id)
    if get_chat_id is None:
        bot.sendMessage(chat_id,
                        text="*Disculpa las molestias*, pero tienes que _volver a configurar el bot_. Escribe /start o púlsalo" \
                             "\n\n*We are sorry*, but you have to _configure again the bot_. Type /start or press on it",
                        parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        lang = db_m.read_lang(chat_id)
        db_m.last_usage(chat_id, datetime.datetime.now().strftime("%H:%M %d-%m-%Y"))
        if path.exists("first_run_{}".format(chat_id)):
            bot.sendMessage(chat_id=chat_id,
                            text="¡Hey! Primero tienes que terminar la configuración inicial\n\nHey! first you have to finish the initial setup")
        elif lang == 'es':
            bot.sendMessage(chat_id=chat_id,
                            text="ᴛéʀᴍɪɴᴏs ᴅᴇ sᴇʀᴠɪᴄɪᴏ ʏ ᴘᴏʟíᴛɪᴄᴀs ᴅᴇ ᴘʀɪᴠᴀᴄɪᴅᴀᴅ" \
                            "\n\nAl utilizar este bot, *aceptas que recopilemos* y guardemos datos sobre ti tales como" \
                            " tu *nombre de usuario*, *zona horaria*, *gustos y preferencias*. Dichos datos no son ni serán" \
                            " *compartidos con terceros* y estarán bajo protección *inclusive cuando el usuario elimine* y" \
                            " *bloquee al bot*. En este caso, se pasará o a la *conservación de los datos* o a la" \
                            " *eliminación de los mismos*, según se convenga.\nCuando el bot recibe una ubicación, por " \
                            "*motivos de seguridad*, primero hay que activar la opción de cambio de zona horaria para" \
                            " evitar cualquier *fuga de datos*. A su vez, la ubicación *solo y únicamente se emplea* para" \
                            " determinar tu zona horaria. Después, *la ubicación enviada se elimina*." \
                            "\n\nPara *cualquier duda*, [contacta conmigo aquí](http://t.me/Javinator_9889) o escríbeme por aquí: @Javinator\\_9889",
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            disable_web_page_preview=True)
        else:
            bot.sendMessage(chat_id=chat_id,
                            text="ᴛᴇʀᴍs ᴏғ sᴇʀᴠɪᴄᴇ ᴀɴᴅ ᴘʀɪᴠᴀᴄʏ ᴘᴏʟɪᴛɪᴄs" \
                                 "\n\nWhen using this bot, *you accept that we save and store* data about you such as" \
                                 " your *username*, *time zone*, *pleasures and preferences*. Those data are not and will" \
                                 " not be *shared with third party entities* and will be under protection *although the*" \
                                 " *user stops and deletes the bot*. In this case, data can be *saved and protected* or" \
                                 " *completely deleted*, as appropriate.\nWhen the bot gets a location, because of " \
                                 "*security reasons*, first you have to active the option of changing time-zone in order to" \
                                 " avoid *data leak*. Also, your location *is single and only used* to" \
                                 " decide your time-zone. Then, *sent location is deleted*." \
                                 "\n\nFor *any doubt*, [contact me here](http://t.me/Javinator_9889) or write me with: @Javinator\\_9889",
                            parse_mode=telegram.ParseMode.MARKDOWN,
                            disable_web_page_preview=True)
