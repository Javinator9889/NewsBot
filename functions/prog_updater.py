import datetime as dt
import pytz
import functions.database_manager as db_m


def next_weekday(day, weekday):
    days_ahead = weekday - day.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return day + dt.timedelta(days_ahead)


def next_day(chat_id, text):
    try:
        t_zone = db_m.get_time_diff(chat_id)
        print("Zona horaria:", t_zone)
        updated_text = text.lower()
        print("Text actualizado:", updated_text)
        if 'lun' in text:
            updated_text = updated_text.replace("lun", "mon")
            day_num = 0
        elif 'mar' in text:
            updated_text = updated_text.replace("mar", "tue")
            day_num = 1
        elif 'mie' in text:
            updated_text = updated_text.replace("mie", "wed")
            day_num = 2
        elif 'jue' in text:
            updated_text = updated_text.replace("jue", "thu")
            day_num = 3
        elif 'vie' in text:
            updated_text = updated_text.replace("vie", "fri")
            day_num = 4
        elif 'sab' in text:
            updated_text = updated_text.replace("sab", "sat")
            day_num = 5
        elif 'dom' in text:
            updated_text = updated_text.replace("dom", "sun")
            day_num = 6
        else:
            day_num = dt.datetime.today().weekday() + 1
            if day_num == 7:
                day_num = 0
        print("Texto final:", updated_text)
        print("Día número:", day_num)
        next_execution = next_weekday(dt.datetime.now(pytz.timezone(t_zone)).date(), day_num)

        print("Próxima ejecución:", next_execution)
        obtained_date = str(next_execution) + " " + updated_text

        print("Fecha obtenida final:", obtained_date)
        local = pytz.timezone(t_zone)
        try:
            naive = dt.datetime.strptime(obtained_date, "%Y-%m-%d %H:%M")
        except ValueError:
            try:
                naive = dt.datetime.strptime(obtained_date, "%Y-%m-%d %H:%M%p")
            except ValueError:
                try:
                    naive = dt.datetime.strptime(obtained_date, "%Y-%m-%d %H:%M %a")
                except ValueError:
                    try:
                        naive = dt.datetime.strptime(obtained_date, "%Y-%m-%d %H:%M%p %a")
                    except ValueError:
                        raise TypeError('Time format is not correct')
        print("Formato strptime:", naive)
        local_dt = local.localize(naive)
        utc_dt = local_dt.astimezone(pytz.timezone("Europe/Madrid"))

        final = utc_dt.strftime("%Y-%m-%d %H:%M %a")

        print("Formato final de tiempo:", final)

        return final
    except TypeError:
        return "Error"
