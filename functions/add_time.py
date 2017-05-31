import datetime
import pytz
import functions.database_manager as db_m


def add_day(text, chat_id, which):
    readed_text = datetime.datetime.strptime(text, "%Y-%m-%d %H:%M %a")
    new_date = (readed_text + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    actual = (db_m.get_time_prog(chat_id)).split(",")

    if which == 1 and len(actual) > 1:
        act = actual[0]
    elif which == 1 and len(actual) < 2:
        act = actual
    elif which == 2:
        act = actual[1]
    else:
        return None

    t_zone = db_m.get_time_diff(chat_id)

    local_next_msg = new_date + " " + act

    local = pytz.timezone(t_zone)

    naive = datetime.datetime.strptime(local_next_msg, "%Y-%m-%d %H:%M")
    local_dt = local.localize(naive)
    utc_dt = local_dt.astimezone(pytz.timezone("Europe/Madrid"))

    final = utc_dt.strftime("%Y-%m-%d %H:%M %a")

    return final


def add_week(text, chat_id, which):
    readed_text = datetime.datetime.strptime(text, "%Y-%m-%d %H:%M %a")
    new_date = (readed_text + datetime.timedelta(weeks=1)).strftime("%Y-%m-%d")

    actual = (db_m.get_time_prog(chat_id)).split(",")
    if which == 1 and len(actual) > 1:
        act = actual[0]
    elif which == 1 and len(actual) < 2:
        act = actual
    elif which == 2:
        act = actual[1]
    else:
        return None

    if 'lun' in act:
        updated_text = act.replace("lun", "mon")
    elif 'mar' in act:
        updated_text = act.replace("mar", "tue")
    elif 'mie' in act:
        updated_text = act.replace("mie", "wed")
    elif 'jue' in act:
        updated_text = act.replace("jue", "thu")
    elif 'vie' in act:
        updated_text = act.replace("vie", "fri")
    elif 'sab' in act:
        updated_text = act.replace("sab", "sat")
    elif 'dom' in act:
        updated_text = act.replace("dom", "sun")
    else:
        updated_text = act

    t_zone = db_m.get_time_diff(chat_id)

    local_next_msg = new_date + " " + updated_text

    local = pytz.timezone(t_zone)

    naive = datetime.datetime.strptime(local_next_msg, "%Y-%m-%d %H:%M %a")
    local_dt = local.localize(naive)
    utc_dt = local_dt.astimezone(pytz.timezone("Europe/Madrid"))

    final = utc_dt.strftime("%Y-%m-%d %H:%M %a")

    return final
