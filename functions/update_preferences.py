import telegram
import os
import os.path as path
import functions.database_manager as db_m
import re


def upd_pref(bot, chat_id, text):
    lang = db_m.read_lang(chat_id)
    if text == "Terminado" or text == "terminado" or text == "Done" or text == "done":
        if path.exists("pref_{}.txt".format(chat_id)):
            pref_file = open("pref_{}.txt".format(chat_id), 'r')
            pref = pref_file.readline()
            pref_file.close()
            os.remove("pref_{}.txt".format(chat_id))
            db_m.update_pref(chat_id, pref)
            if lang == 'es':
                bot.sendMessage(chat_id,
                                "Perfecto, hemos actualizado tus preferencias")
            else:
                bot.sendMessage(chat_id,
                                "Perfect, everything is updated")
        else:
            if lang == 'es':
                bot.sendMessage(chat_id,
                                "No se ha realizado ningún cambio")
            else:
                bot.sendMessage(chat_id,
                                "No changes were done")
        db_m.is_pref(chat_id, False)
    elif text == "Cancelar" or text == "cancelar" or text == "Cancell" or text == "cancell":
        if path.exists("pref_{}.txt".format(chat_id)):
            os.remove("pref_{}.txt".format(chat_id))
        db_m.is_pref(chat_id, False)
        if lang == 'es':
            bot.sendMessage(chat_id,
                            "Se ha cancelado la actualización de las preferencias")
        else:
            bot.sendMessage(chat_id,
                            "Updating preferences cancelled")
    elif 'Eliminar' in text or 'eliminar' in text:
        if path.exists("pref_{}.txt".format(chat_id)):
            file = open("pref_{}.txt".format(chat_id), 'r')
            saved_pref = file.readline()
            file.close()
            if saved_pref == '':
                err = True
            else:
                pref_list = saved_pref.split(",")
                out = [var for var in pref_list if var]
                err = False
        else:
            saved_pref = db_m.get_pref(chat_id)
            if saved_pref == '':
                err = True
            else:
                pref_list = saved_pref.split(",")
                out = [var for var in pref_list if var]
                err = False
        delete = text[9:]
        delete_list = delete.split(",")
        # print(delete_list, out)
        deleting = []
        if err is True:
            if lang == 'es':
                bot.sendMessage(chat_id,
                                "No puedes eliminar nada más...")
            else:
                bot.sendMessage(chat_id,
                                "You can't delete anything else...")
        else:
            for k in range(0, len(delete_list)):
                elem = int(delete_list[k]) - 1
                try:
                    deleting.append(out[elem])
                except (ValueError, IndexError, KeyError):
                    bot.sendMessage(chat_id, "...")
            for x in range(0, len(deleting)):
                print(deleting[x], len(deleting))
                try:
                    out.remove(deleting[x])
                    out = [var for var in out if var]
                except (ValueError, IndexError, KeyError):
                    bot.sendMessage(chat_id, "...")
            # print(out)
            write_file = open("pref_{}.txt".format(chat_id), 'w')
            for item in out:
                write_file.write("%s," % item)
            write_file.close()
            if len(out) == 0:
                if lang == 'es':
                    comp_list = "_vacío_"
                else:
                    comp_list = "_empty"
            else:
                for a in range(0, len(out)):
                    lst = re.findall(r'"(.*?)(?<!\\)"', out[a])
                    if a == 0:
                        try:
                            comp_list = "*" + str(a + 1) + "*: " + "_" + lst[0] + "_" + "\n"
                        except IndexError:
                            comp_list = "*" + str(a + 1) + "*: " + "_" + out[a] + "_" + "\n"
                    else:
                        if out[a] != '':
                            try:
                                comp_list += "*" + str(a + 1) + "*: " + "_" + lst[0] + "_" + "\n"
                            except IndexError:
                                comp_list += "*" + str(a + 1) + "*: " + "_" + out[a] + "_" + "\n"
            if lang == 'es':
                bot.sendMessage(chat_id=chat_id,
                                text="_Estado actual de tus preferencias:_\n\n" + comp_list + "",
                                parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.sendMessage(chat_id=chat_id,
                                text="_Current status of your preferences:_\n\n" + comp_list + "",
                                parse_mode=telegram.ParseMode.MARKDOWN)
    elif 'Delete' in text or 'delete' in text:
        if path.exists("pref_{}.txt".format(chat_id)):
            file = open("pref_{}.txt".format(chat_id), 'r')
            saved_pref = file.readline()
            file.close()
            if saved_pref == '':
                err = True
            else:
                pref_list = saved_pref.split(",")
                out = [var for var in pref_list if var]
                err = False
        else:
            saved_pref = db_m.get_pref(chat_id)
            if saved_pref == '':
                err = True
            else:
                pref_list = saved_pref.split(",")
                out = [var for var in pref_list if var]
                err = False
        delete = text[7:]
        delete_list = delete.split(",")
        # print(delete_list, out)
        deleting = []
        if err is True:
            if lang == 'es':
                bot.sendMessage(chat_id,
                                "No puedes eliminar nada más...")
            else:
                bot.sendMessage(chat_id,
                                "You can't delete anything else...")
        else:
            for k in range(0, len(delete_list)):
                try:
                    elem = int(delete_list[k]) - 1
                    deleting.append(out[elem])
                except (ValueError, IndexError, KeyError):
                    bot.sendMessage(chat_id, "...")
            for x in range(0, len(deleting)):
                # print(deleting[x], len(deleting))
                try:
                    out.remove(deleting[x])
                    out = [var for var in out if var]
                except ValueError:
                    bot.sendMessage(chat_id, "...")
            # print(out)
            write_file = open("pref_{}.txt".format(chat_id), 'w')
            for item in out:
                write_file.write("%s," % item)
            write_file.close()
            if len(out) == 0:
                if lang == 'es':
                    comp_list = "_vacío_"
                else:
                    comp_list = "_empty_"
            else:
                for a in range(0, len(out)):
                    lst = re.findall(r'"(.*?)(?<!\\)"', out[a])
                    if a == 0:
                        try:
                            comp_list = "*" + str(a + 1) + "*: " + "_" + lst[0] + "_" + "\n"
                        except IndexError:
                            comp_list = "*" + str(a + 1) + "*: " + "_" + out[a] + "_" + "\n"
                    else:
                        if out[a] != '':
                            try:
                                comp_list += "*" + str(a + 1) + "*: " + "_" + lst[0] + "_" + "\n"
                            except IndexError:
                                comp_list += "*" + str(a + 1) + "*: " + "_" + out[a] + "_" + "\n"
            if lang == 'es':
                bot.sendMessage(chat_id=chat_id,
                                text="_Estado actual de tus preferencias:_\n\n" + comp_list + "",
                                parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.sendMessage(chat_id=chat_id,
                                text="_Current status of your preferences:_\n\n" + comp_list + "",
                                parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        if path.exists("pref_{}.txt".format(chat_id)):
            file = open("pref_{}.txt".format(chat_id), 'r')
            saved_pref = file.readline()
            file.close()
            if saved_pref == '':
                out = []
            else:
                pref_list = saved_pref.split(",")
                out = [var for var in pref_list if var]
        else:
            saved_pref = db_m.get_pref(chat_id)
            if saved_pref == '':
                out = []
            else:
                pref_list = saved_pref.split(",")
                out = [var for var in pref_list if var]
        new_pref = text.split(",")
        print(new_pref)
        a = len(new_pref)
        for v in range(0, a):
            if new_pref[v] not in out:
                out.append(new_pref[v])
        print(out)
        save_file = open("pref_{0}.txt".format(chat_id), 'w')
        for x in range(0, len(out)):
            save_file.write(out[x] + ",")
        save_file.close()
        if len(out) == 0:
            if lang == 'es':
                comp_list = "_vacío_"
            else:
                comp_list = "_empty"
        else:
            for a in range(0, len(out)):
                lst = re.findall(r'"(.*?)(?<!\\)"', out[a])
                if a == 0:
                    try:
                        comp_list = "*" + str(a + 1) + "*: " + "_" + lst[0] + "_" + "\n"
                    except IndexError:
                        comp_list = "*" + str(a + 1) + "*: " + "_" + out[a] + "_" + "\n"
                else:
                    if out[a] != '':
                        try:
                            comp_list += "*" + str(a + 1) + "*: " + "_" + lst[0] + "_" + "\n"
                        except IndexError:
                            comp_list += "*" + str(a + 1) + "*: " + "_" + out[a] + "_" + "\n"
        if lang == 'es':
            bot.sendMessage(chat_id=chat_id,
                            text="_Estado actual de tus preferencias:_\n\n" + comp_list + "",
                            parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.sendMessage(chat_id=chat_id,
                            text="_Current status of your preferences:_\n\n" + comp_list + "",
                            parse_mode=telegram.ParseMode.MARKDOWN)
