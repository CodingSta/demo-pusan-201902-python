#
# 파이썬 텔레그램 봇 서버
#


import os
import re
import sys
import traceback
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler
import requests
from bs4 import BeautifulSoup


def naver_blog_search(keyword):
    search_url = "https://search.naver.com/search.naver"
    params = {
        'where': 'post',
        'query': keyword,
    }

    res = requests.get(search_url, params=params)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    tag_list = soup.select('.sh_blog_title')

    for tag in tag_list:
        post_url = tag['href']
        post_title = tag['title']
        post = {
            'title': post_title,
            'url': post_url,
        }
        yield post


def start(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    bot.send_message(chat_id=chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
    chat_id = update.message.chat_id  # 대화방 ID
    text = update.message.text

    try:
        matched = re.match(r"네이버에?서?\s*(.+)\s*검색", text)
        if matched:
            keyword = matched.groups()[0]
            line_list = []
            for post in naver_blog_search(keyword):
                # line = "{}\n{}".format(post['title'], post['url'])
                line = "{title}\n{url}".format(**post)
                line_list.append(line)
            response = '\n\n'.join(line_list)
        elif text == '야':
            response = '왜?'
        else:
            response = '니가 무슨 말 하는 지 모르겠어. :('
    except Exception as e:
        response = '처리 중에 오류가 발생했어요. :('
        traceback.print_exc()

    bot.send_message(chat_id=chat_id, text=response)


def main(token):
    bot = Updater(token=TOKEN)

    handler = CommandHandler('start', start)
    bot.dispatcher.add_handler(handler)

    handler = MessageHandler(Filters.text, echo)
    bot.dispatcher.add_handler(handler)

    bot.start_polling()

    print('running telegram bot ...')
    bot.idle()


if __name__ == '__main__':
    # TODO: 필요한 라이브러리 설치 : pip install python-telegram-bot requests beautifulsoup4
    # FIXME: 각자의 Token을 적용해주세요.
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    if TOKEN is None:
        print('ERROR) TELEGRAM_TOKEN을 지정해주세요.', file=sys.stderr)
        sys.exit(1)
    main(TOKEN)

