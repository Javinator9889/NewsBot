#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging                                                                          # Standard python libraries
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler                  # python-telegram-bot library
from telegram.ext import MessageHandler, Filters                                        # python-telegram-bot library
from telegram.ext import InlineQueryHandler
import telegram
import datetime as dt
import pytz
import functions.start_handler as st
import functions.text_message_handler as msg
import functions.callback_handler as ch
import functions.help as hp
import functions.inline_query as inlinequery
import functions.preferences as pf
import functions.database_manager as db_m
import functions.add_time as add_time
import functions.location_handler as lc
import functions.programation_func as prog
import functions.developers as dev
import functions.privacy_politics as priv
import functions.nothing as nothing
import functions.errors as err
import time                                                                             # Standard python libraries


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',    # Starting logging at WARNING level (for errors information)
                    level=logging.INFO)

token_file = open("TOKEN.txt", 'r')
token = token_file.readline()
token_file.close()

updater = Updater(token, workers=200)
dispatcher = updater.dispatcher

# Initialize "Command" handlers
start_handler = CommandHandler('start', st.start)
dispatcher.add_handler(start_handler)
help_handler = CommandHandler('help', hp.help_handler)
dispatcher.add_handler(help_handler)
echo_handler = MessageHandler(Filters.text, msg.echo)
dispatcher.add_handler(echo_handler)
loc_handler = MessageHandler(Filters.location, lc.location)
dispatcher.add_handler(loc_handler)
pref_handler = CommandHandler('preferences', pf.key_pref)
dispatcher.add_handler(pref_handler)
dev_handler = CommandHandler('develop', dev.develop)
dispatcher.add_handler(dev_handler)
priv_handler = CommandHandler('privacy', priv.policy)
dispatcher.add_handler(priv_handler)
err_handler = CommandHandler('issues', err.issues)
dispatcher.add_handler(err_handler)
photo_handler = MessageHandler(Filters.photo, nothing.photo)
dispatcher.add_handler(photo_handler)
video_handler = MessageHandler(Filters.video, nothing.video)
dispatcher.add_handler(video_handler)
song_handler = MessageHandler(Filters.audio, nothing.song)
dispatcher.add_handler(song_handler)
voice_handler = MessageHandler(Filters.voice, nothing.voice)
dispatcher.add_handler(voice_handler)
nothing_handler = MessageHandler((Filters.sticker | Filters.contact | Filters.document), nothing.nothing)
dispatcher.add_handler(nothing_handler)

# Handler for queries
dispatcher.add_handler(InlineQueryHandler(inlinequery.inlinequery))


# Initialize "button" 'CallbackQueryHandler' required for InlineKeyborads
updater.dispatcher.add_handler(CallbackQueryHandler(ch.callb_button))

# Starts "updater" in order to getting updates and messages from Telegram servers
updater.start_polling(timeout=30)
print("Starting bot...\n\n")

print("Iniciando programación...")

print("NewsBot (Telegram)  Copyright (C) 2017  Javinator9889\n\n\
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.\n\
This is free software, and you are welcome to redistribute it\
under certain conditions; type `show c' for details.")

try:
    while 1:
        data = db_m.fetch_chatids_progtimes()
        if data is False:
            print("No users registered yet")
        else:
            for row in data:
                try:
                    times = row[1].split(",")
                except AttributeError:
                    times = []
                try:
                    if times[0] == dt.datetime.now(pytz.timezone("Europe/Madrid")).strftime("%Y-%m-%d %H:%M %a"):
                        print("Sending news to", row[0], "at time:", dt.datetime.now(pytz.timezone("Europe/Madrid"))\
                              .strftime("\"%H:%M, %d-%m-%Y on %A\""))
                        prog.prog(updater.bot, updater, row[0])
                        prog_hours = db_m.get_time_prog(row[0]).lower().split(",")
                        if 'lun' in prog_hours[0] or 'mar' in prog_hours[0] or 'mie' in prog_hours[0] or\
                                'jue' in prog_hours[0] or 'vie' in prog_hours[0] or 'sab' in prog_hours[0] or\
                                'dom' in prog_hours[0] or 'mon' in prog_hours[0] or 'tue' in prog_hours[0] or\
                                'wed' in prog_hours[0] or 'thu' in prog_hours[0] or 'fri' in prog_hours[0] or\
                                'sat' in prog_hours[0] or 'sun' in prog_hours[0]:
                            next_time = add_time.add_week(times[0], row[0], 1)
                        else:
                            next_time = add_time.add_day(times[0], row[0], 1)
                        if times[1] is not None:
                            final_time = next_time + "," + times[1]
                        else:
                            final_time = next_time
                        db_m.update_prog_time(final_time, row[0])
                    elif times[1] == dt.datetime.now(pytz.timezone("Europe/Madrid")).strftime("%Y-%m-%d %H:%M %a"):
                        print("Sending news to", row[0], "at time:", dt.datetime.now(pytz.timezone("Europe/Madrid")) \
                              .strftime("\"%H:%M, %d-%m-%Y on %A\""))
                        prog.prog(updater.bot, updater, row[0])
                        prog_hours = db_m.get_time_prog(row[0]).lower().split(",")
                        if 'lun' in prog_hours[1] or 'mar' in prog_hours[1] or 'mie' in prog_hours[1] or \
                                        'jue' in prog_hours[1] or 'vie' in prog_hours[1] or 'sab' in prog_hours[1] or \
                                        'dom' in prog_hours[1] or 'mon' in prog_hours[1] or 'tue' in prog_hours[1] or \
                                        'wed' in prog_hours[1] or 'thu' in prog_hours[1] or 'fri' in prog_hours[1] or \
                                        'sat' in prog_hours[1] or 'sun' in prog_hours[1]:
                            next_time = add_time.add_week(times[1], row[0], 2)
                        else:
                            next_time = add_time.add_day(times[1], row[0], 2)
                        if times[0] is not None:
                            final_time = times[0] + "," + next_time
                        else:
                            final_time = next_time
                        db_m.update_prog_time(final_time, row[0])
                except IndexError:
                    # print("Values for", row[0], "are not set-up")
                    pass
        time.sleep(10)
except (KeyboardInterrupt, TypeError):
    updater.idle()        # Stops the bot only with "Ctrl+C" on keyboard
    print("\nBot detenido\nFinalizando...")

# The next message has to be included in every copy of this program, modified or not
""" NewsBot (Telegram) -- A simple bot for getting news from Google
    Copyright (C) 2017  Javinator9889

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    For contacting, go to "https://github.com/Javinator9889/NewsBot/issues" and type your message.
    Also you can go to my GitHub profile and send me direct message.
"""
