from telegram import InlineQueryResultArticle
from telegram import InputTextMessageContent
from telegram.ext.dispatcher import run_async
import telegram
import gsearch
from uuid import uuid4
from bs4 import BeautifulSoup
import urllib.request as rq
import time
from functions.title_finder import title as title_finder


def handler(signo, frame):
    raise OSError('Time-out reached')


@run_async
def inlinequery(bot, update):
    query = update.inline_query.query
    print(query, query[3:])
    results_list = list()
    if 'en,' in query:
        lang = "en"
        flag = 0
    elif 'es,' in query:
        lang = "es"
        flag = 0
    elif query == 'share es':
        flag = 2
    elif query == 'share en':
        flag = 3
    else:
        flag = 1
    if flag == 0:
        results = gsearch.search_news(lang=lang, query=query[3:], num=10)
        news = results[0]
        print(news)
        if news.get("Page {}".format(1)) is None:
            if lang == 'es':
                print("lang = es")
                results_list.append(InlineQueryResultArticle(
                    id=uuid4(),
                    title="❌ No se han encontrado resultados ❌",
                    description="No se ha encontrado nada en base a tus términos de búsqueda",
                    input_message_content=InputTextMessageContent(
                        message_text="Por favor, prueba con otros términos de búsqueda",
                        parse_mode=telegram.ParseMode.MARKDOWN,
                    )
                ))
            else:
                print("lang = en")
                results_list.append(InlineQueryResultArticle(
                    id=uuid4(),
                    title="❌ No results found ❌",
                    description="There are no results with your search terms",
                    input_message_content=InputTextMessageContent(
                        message_text="Please, try with another search terms",
                        parse_mode=telegram.ParseMode.MARKDOWN,
                    )
                ))
        else:
            for u in range(1, results[1]):
                page = news.get("Page {}".format(u))
                title = title_finder(page)
                if title is None:
                    title = page
                else:
                    title = title.replace('\n', '').replace('\r', '').replace('\t', ''). \
                        replace('*', '\\*').replace('`', '\\`').replace('[', '\\[').replace(']', '\\]')
                    title = ' '.join(title.split())
                    print(u, title)
                results_list.append(InlineQueryResultArticle(
                    id=uuid4(),
                    title=title,
                    description="Powered by NewsBot",
                    input_message_content=InputTextMessageContent(
                        message_text="*{0}*\n[Link]({1}) 🔗".format(title, page),
                        parse_mode=telegram.ParseMode.MARKDOWN,
                        disable_web_page_preview=False,
                    )
                ))
    elif flag == 2:
        results_list.append(InlineQueryResultArticle(
            id=uuid4(),
            title="👇 Pulsa para compartir el bot 👇",
            description="NewsBot",
            input_message_content=InputTextMessageContent(
                message_text="¡Mira qué bot tan genial! 😱\n\nRecopila *cualquier noticia* 🗞 y además se _puede programar_\
        \n\n*PRUÉBALO AQUÍ*: @GooglNews\\_bot O en [este enlace](https://telegram.me/googlnews_bot)",
                parse_mode=telegram.ParseMode.MARKDOWN,
            )
        ))
    elif flag == 3:
        results_list.append(InlineQueryResultArticle(
            id=uuid4(),
            title="👇 Press to share the bot 👇",
            description="NewsBot",
            input_message_content=InputTextMessageContent(
                message_text="Look such a great bot! 😱\n\nIt looks for *every news* 🗞 and it can be _scheduled_\
        \n\n*CHECK IT OUT*: @GooglNews\\_bot OR at [this link](https://telegram.me/googlnews_bot)",
                parse_mode=telegram.ParseMode.MARKDOWN,
            )
        ))
    else:
        print("No language")
        results_list.append(InlineQueryResultArticle(
            id=uuid4(),
            title="Please, define your language ❌",
            description="Format: \n- para español: es,término\n- for English: en,search term",
            input_message_content=InputTextMessageContent(
                message_text="*Please, define your language typing* \
        `@GooglNews_bot lang,search_terms`\n\nPor favor, define tu idioma escribiendo `@GooglNews_bot \
        idioma,términos_búsqueda`",
                parse_mode=telegram.ParseMode.MARKDOWN,
            )
        ))

    bot.answerInlineQuery(update.inline_query.id, results=results_list, cache_time=0, timeout=30)
