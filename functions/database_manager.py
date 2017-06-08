import pymysql
from functions.db_connection import db_connection


def r_w_chat_id(chat_id, user):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    c.execute("""SELECT chat_id FROM NewsBot WHERE chat_id = %s""", chat_id)
    db_chat_id = c.fetchone()

    if db_chat_id is None:
        c.execute("INSERT INTO NewsBot (chat_id) VALUES (%s)", chat_id)
        c.execute("""UPDATE NewsBot SET usr_name = %s WHERE chat_id = %s""", (user, chat_id))
        db.commit()
        db.close()
        return "Updated"
    else:
        db.close()
        return "In_db"


def read_chatid(chat_id):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    c.execute("""SELECT chat_id FROM NewsBot WHERE chat_id = %s""", chat_id)
    db_chat_id = c.fetchone()

    if db_chat_id is None:
        return None
    else:
        return "In database"


def read_lang(chat_id):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    c.execute("""SELECT lang FROM NewsBot WHERE chat_id = %s""", chat_id)
    db_lang = c.fetchone()

    db.close()
    if db_lang is None:
        return None
    else:
        lang = db_lang[0]
        return lang


def write_lang(chat_id, lang):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    c.execute("""UPDATE NewsBot SET lang = %s WHERE chat_id = %s""", (lang, chat_id))

    db.commit()

    db.close()


def get_time_diff(chat_id):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    c.execute("""SELECT diff_time FROM NewsBot WHERE chat_id = %s""", chat_id)
    db_diff = c.fetchone()

    db.close()
    if db_diff is None:
        return None
    else:
        diff = db_diff[0]
        return diff


def is_time(chat_id, change):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    if change is True:
        c.execute("""UPDATE NewsBot SET is_time = %s WHERE chat_id = %s""", (change, chat_id))
        db.commit()
        db.close()
    elif change is False:
        c.execute("""UPDATE NewsBot SET is_time = %s WHERE chat_id = %s""", (change, chat_id))
        db.commit()
        db.close()
    elif change is None:
        c.execute("""SELECT is_time FROM NewsBot WHERE chat_id = %s""", chat_id)
        db_time = c.fetchone()

        db.close()

        if db_time is None:
            return None
        else:
            changing_time = db_time[0]
            return changing_time


def update_time(chat_id, time):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    c.execute("""UPDATE NewsBot SET diff_time = %s WHERE chat_id = %s""", (time, chat_id))

    db.commit()
    db.close()


def is_pref(chat_id, change):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    if change is True:
        c.execute("""UPDATE NewsBot SET is_pref = %s WHERE chat_id = %s""", (change, chat_id))
        db.commit()
        db.close()
    elif change is False:
        c.execute("""UPDATE NewsBot SET is_pref = %s WHERE chat_id = %s""", (change, chat_id))
        db.commit()
        db.close()
    elif change is None:
        c.execute("""SELECT is_pref FROM NewsBot WHERE chat_id = %s""", chat_id)
        db_pref = c.fetchone()

        db.close()

        if db_pref is None:
            return None
        else:
            changing_pref = db_pref[0]
            return changing_pref


def get_pref(chat_id):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    c.execute("""SELECT preferences FROM NewsBot WHERE chat_id = %s""", chat_id)
    db_pref = c.fetchone()

    db.close()

    if db_pref is None:
        return []
    else:
        pref = db_pref[0]
        return pref


def update_pref(chat_id, preferences):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    c.execute("""UPDATE NewsBot SET preferences = %s WHERE chat_id = %s""", (preferences, chat_id))

    db.commit()
    db.close()


def is_prog(chat_id, change):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    if change is True:
        c.execute("""UPDATE NewsBot SET is_prog = %s WHERE chat_id = %s""", (change, chat_id))
        db.commit()
        db.close()
    elif change is False:
        c.execute("""UPDATE NewsBot SET is_prog = %s WHERE chat_id = %s""", (change, chat_id))
        db.commit()
        db.close()
    elif change is None:
        c.execute("""SELECT is_prog FROM NewsBot WHERE chat_id = %s""", chat_id)
        db_prog = c.fetchone()

        db.close()

        if db_prog is None:
            return None
        else:
            changing_prog = db_prog[0]
            return changing_prog


def get_time_prog(chat_id):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    c.execute("""SELECT programation FROM NewsBot WHERE chat_id = %s""", chat_id)
    db_pref = c.fetchone()

    db.close()

    if db_pref is None:
        return None
    else:
        time = db_pref[0]
        return time


def update_prog(chat_id, prog_hours):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    c.execute("""UPDATE NewsBot SET programation = %s WHERE chat_id = %s""", (prog_hours, chat_id))

    db.commit()
    db.close()


def last_msgid(chat_id, message_id):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    c.execute("""UPDATE NewsBot SET msg_id = %s WHERE chat_id = %s""", (message_id, chat_id))

    db.commit()
    db.close()


def read_last_msgid(chat_id):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    c.execute("""SELECT msg_id FROM NewsBot WHERE chat_id = %s""", chat_id)
    db_msg = c.fetchone()

    db.close()

    if db_msg is None:
        return None
    else:
        message_id = db_msg[0]
        return message_id


def get_max(chat_id):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    c.execute("""SELECT max_results FROM NewsBot WHERE chat_id = %s""", chat_id)
    db_max = c.fetchone()

    db.close()

    if db_max is None:
        return None
    else:
        max_r = db_max[0]
        return max_r


def update_max(value, chat_id):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    c.execute("""UPDATE NewsBot SET max_results = %s WHERE chat_id = %s""", (value, chat_id))

    db.commit()
    db.close()


def read_prog(chat_id):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    c.execute("""SELECT next_prog FROM NewsBot WHERE chat_id = %s""", chat_id)
    db_time = c.fetchone()

    db.close()

    if db_time is None:
        return None
    else:
        max_r = db_time[0]
        return max_r


def update_prog_time(value, chat_id):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    c.execute("""UPDATE NewsBot SET next_prog = %s WHERE chat_id = %s""", (value, chat_id))

    db.commit()
    db.close()


def fetch_chatids_progtimes():
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    c.execute("""SELECT chat_id, next_prog FROM NewsBot""")

    db_values = c.fetchall()

    db.close()

    if db_values:
        return db_values
    else:
        return False


def last_usage(chat_id, time):
    db = db_connection()
    c = db.cursor()
    0
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    c.execute("""UPDATE NewsBot SET last_time = %s WHERE chat_id = %s""", (time, chat_id))

    db.commit()
    db.close()
