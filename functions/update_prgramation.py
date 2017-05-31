import datetime
import telegram
import os
import os.path as path
import functions.database_manager as db_m


def update_time(bot, chat_id, text):
    lang = db_m.read_lang(chat_id)
    currently_setup = db_m.get_time_prog(chat_id)
    if currently_setup is None:
        prog_list = []
    else:
        prog_list = currently_setup.split(",")
    print(prog_list)
    try:
        if len(prog_list) > 1:
            raise TabError('Only set-up two different times')
        """time_1 = text.lower().replace("lun", "mon").replace("mar", "tue").replace("mie", "thu").replace("jue", "thu")\
            .replace("vie", "fri").replace("sab", "sat").replace("dom", "sun")"""
        time = text.split(",")
        print(time, len(time))
        days = {0: "mon", 1: "tue", 2: "wed", 3: "thu", 4: "fri", 5: "sat", 6: "sun"}
        dias = {0: "lun", 1: "mar", 2: "mie", 3: "jue", 4: "vie", 5: "sab", 6: "dom"}
        weekday = None
        other_wd = None
        for a in range(0, len(time)):
            current = time[a]
            print(current)
            for m in range(0, 6):
                if lang == 'en':
                    if days.get(m) in current:
                        if a == 0:
                            weekday = days.get(m)
                            num_day = m
                        elif a == 1:
                            other_wd = days.get(m)
                            num_day_2 = m
                else:
                    if dias.get(m) in current:
                        if a == 0:
                            weekday = days.get(m)
                            num_day = m
                        elif a == 1:
                            other_wd = days.get(m)
                            num_day_2 = m
        print(weekday, other_wd)
        if len(time) > 1:
            try:
                check_time = datetime.datetime.strptime(time[0], "%H:%M")
                typo_1 = 0
            except ValueError:
                try:
                    check_time = datetime.datetime.strptime(time[0], "%I:%M%p")
                    typo_1 = 0
                except ValueError:
                    try:
                        check_time = datetime.datetime.strptime(time[0].replace(dias.get(num_day), days.get(num_day)), "%H:%M %a")
                        typo_1 = 1
                    except ValueError:
                        try:
                            check_time = datetime.datetime.strptime(time[0].replace(dias.get(num_day), days.get(num_day)), "%I:%M%p %a")
                            typo_1 = 1
                        except ValueError:
                            raise TypeError('Time format is not correct')
            else:
                try:
                    check_time_2 = datetime.datetime.strptime(time[1], "%H:%M")
                    typo_2 = 0
                except ValueError:
                    try:
                        check_time_2 = datetime.datetime.strptime(time[1], "%I:%M%p")
                        typo_2 = 0
                    except ValueError:
                        try:
                            check_time_2 = datetime.datetime.strptime(time[1].replace(dias.get(num_day_2), days.get(num_day_2)), "%H:%M %a")
                            typo_2 = 1
                        except ValueError:
                            try:
                                check_time_2 = datetime.datetime.strptime(time[1].replace(dias.get(num_day_2), days.get(num_day_2)), "%I:%M%p %a")
                                typo_2 = 1
                            except ValueError:
                                raise TypeError('Time format is not correct')
        else:
            try:
                check_time = datetime.datetime.strptime(time[0], "%H:%M")
                typo_1 = 0
            except ValueError:
                try:
                    check_time = datetime.datetime.strptime(time[0], "%I:%M%p")
                    typo_1 = 0
                except ValueError:
                    try:
                        check_time = datetime.datetime.strptime(time[0], "%H:%M {}".format(weekday))
                        typo_1 = 1
                    except ValueError:
                        try:
                            check_time = datetime.datetime.strptime(time[0], "%I:%M%p {}".format(weekday))
                            typo_1 = 1
                        except ValueError:
                            raise TypeError('Time format is not correct')
        time_diff = db_m.get_time_diff(chat_id)
        print(time_diff, check_time, check_time_2)

        if time_diff > 0 and len(time) > 1:
            updated_time_1 = check_time - datetime.timedelta(hours=time_diff)
            updated_time_2 = check_time_2 - datetime.timedelta(hours=time_diff)

            if weekday is not None:
                if '-1 day' in str(updated_time_1):
                    weekday = days.get(num_day + 1)
                server_time_1 = updated_time_1.strftime("%H:%M {}".format(weekday))
            elif other_wd is not None:
                if '-1 day' in str(updated_time_2):
                    other_wd = days.get(num_day_2 + 1)
                server_time_2 = updated_time_2.strftime("%H:%M {}".format(other_wd))
            else:
                server_time_1 = updated_time_1.strftime("%H:%M")
                server_time_2 = updated_time_2.strftime("%H:%M")
        elif time_diff < 0 and len(time) > 1:
            updated_time_1 = check_time + datetime.timedelta(hours=-time_diff)
            updated_time_2 = check_time_2 + datetime.timedelta(hours=-time_diff)

            day_compensator = updated_time_1 - check_time
            day_compensator_2 = updated_time_2 - check_time_2

            if weekday is not None:
                if '-1 day' in day_compensator:
                    weekday = days.get(num_day - 1)
                server_time_1 = updated_time_1.strftime("%H:%M {}".format(weekday))
            elif other_wd is not None:
                if '-1 day' in day_compensator_2:
                    other_wd = days.get(num_day_2 - 1)
                server_time_2 = updated_time_2.strftime("%H:%M {}".format(other_wd))
            else:
                server_time_1 = updated_time_1.strftime("%H:%M")
                server_time_2 = updated_time_2.strftime("%H:%M")
        elif time_diff > 0 and len(time) == 1:
            updated_time_1 = check_time - datetime.timedelta(hours=time_diff)

            if weekday is not None:
                if '-1 day' in str(updated_time_1):
                    weekday = days.get(num_day + 1)
                server_time_1 = updated_time_1.strftime("%H:%M {}".format(weekday))
            else:
                server_time_1 = updated_time_1.strftime("%H:%M")
        elif time_diff < 0 and len(time) == 1:
            updated_time_1 = check_time - datetime.timedelta(hours=time_diff)

            day_compensator = updated_time_1 - check_time

            if weekday is not None:
                if '-1 day' in day_compensator:
                    weekday = days.get(num_day - 1)
                server_time_1 = updated_time_1.strftime("%H:%M {}".format(weekday))
            else:
                server_time_1 = updated_time_1.strftime("%H:%M")

        print(server_time_1, server_time_2)

        if len(time) > 1:
            updated_scheduler = server_time_1 + "," + server_time_2
        else:
            updated_scheduler = server_time_1 + ","

        print(updated_scheduler)

        db_m.update_prog(chat_id, updated_scheduler)
        db_m.is_prog(chat_id, False)

        if lang == 'es':
            if len(time) > 1:
                bot.sendMessage(chat_id,
                                text="Se han programado correctamente las horas siguientes: *{} y {}*".format(time[0],
                                                                                                              time[1]),
                                parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.sendMessage(chat_id,
                                text="Se ha programado correctamente la hora siguiente: *{}*".format(time[0]),
                                parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            if len(time) > 1:
                bot.sendMessage(chat_id,
                                text="Time was updated and scheduled correctly at these hours: *{} y {}*".format(
                                    time[0],
                                    time[1]),
                                parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.sendMessage(chat_id,
                                text="Time was updated and scheduled correctly at this hour: *{}*".format(time[0]),
                                parse_mode=telegram.ParseMode.MARKDOWN)

    except TypeError:
        if lang == 'es':
            bot.sendMessage(chat_id, "El formato de tiempo que has especificado no es correcto. \
Por favor, envíalo así: `14:15 dom (HH:MM día)` ó `2:15PM (H:MMAM/PM)`",
                            parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.sendMessage(chat_id, "The specified time format is not correct. \
Please, use this: `14:15 Mon (HH:MM day)` or `2:15PM (H:MMAM/PM)`",
                            parse_mode=telegram.ParseMode.MARKDOWN)
        db_m.is_prog(chat_id, False)

    except TabError:
        if lang == 'es':
            bot.sendMessage(chat_id, "Solo se pueden programar dos tiempos distintos. Borra alguno y prueba de nuevo",
                            parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.sendMessage(chat_id, "Only two different times can be scheduled. Remove someone and try again",
                            parse_mode=telegram.ParseMode.MARKDOWN)
        db_m.is_prog(chat_id, False)
