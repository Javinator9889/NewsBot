# NewsBot
Telegram bot for looking for news. Has scheduling and preferences

## Installing

1. First, you have to create a table in **MySQL** like this:
+--------------+---------------+------+-----+---------+-------+
| Field        | Type          | Null | Key | Default | Extra |
+--------------+---------------+------+-----+---------+-------+
| chat_id      | int(15)       | NO   | PRI | NULL    |       |
| lang         | char(2)       | YES  |     | NULL    |       |
| preferences  | varchar(1000) | YES  |     | NULL    |       |
| diff_time    | varchar(50)   | YES  |     | NULL    |       |
| is_time      | varchar(5)    | YES  |     | NULL    |       |
| programation | varchar(150)  | YES  |     | NULL    |       |
| is_prog      | varchar(5)    | YES  |     | NULL    |       |
| is_pref      | varchar(5)    | YES  |     | NULL    |       |
| msg_id       | int(20)       | YES  |     | NULL    |       |
| max_results  | int(3)        | YES  |     | NULL    |       |
| next_prog    | varchar(150)  | YES  |     | NULL    |       |
| usr_name     | varchar(150)  | YES  |     | NULL    |       |
+--------------+---------------+------+-----+---------+-------+

Use:
`CREATE TABLE NewsBot (

--> usr_name VARCHAR(150),

--> chat_id INT(15) NOT NULL PRIMARY KEY,

--> lang CHAR(2),

--> diff_time VARCHAR(50),

--> preferences VARCHAR(10000),

--> programation VARCHAR(150),

--> next_prog VARCHAR(150),

--> msg_id INT(20),

--> max_results INT(3),

--> is_time VARCHAR(5),

--> is_prog VARCHAR(5),

--> is_pref VARCHAR(5)

);`

2. Then, ask [BotFather](http://t.me/BotFather) for a TOKEN unique for your bot.
3. Save that token into a file called *TOKEN.txt*.
4. Go to [this Google page](https://developers.google.com/maps/documentation/geocoding/start) and ask for your API-KEY. Save it in *API-KEY_geo.txt* (don't forget to activate your API).
5. Go to [this another Google page](https://developers.google.com/maps/documentation/timezone/start) and ask for your API-KEY. Save it in *API-KEY.txt* (don't forget to activate your API).

**It's done**, you have finished your initial set-up

## Requirements
Install this packages with `pip` (using Python 3):
* `pip install PyMySQL`
* `pip install python-telegram-bot`
* `pip install py-GSearch-API`
* `pip install bs4`
* `pip install ujson`
* `pip install unidecode`
* `pip install URLEncoder`
* `pip install requests`
* `pip install html`
* `pip install contextlib`

When finished, everything is now set-up.

## Usage
Just execute `python bot.py` and the bot will start 😄

## License
### The next message has to be included in every copy of this program, modified or not
    NewsBot (Telegram) -- A simple bot for getting news from Google
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
