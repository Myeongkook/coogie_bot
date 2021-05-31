import random
from datetime import datetime
from googleapiclient.discovery import build
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from datetime import date
import requests
from bs4 import BeautifulSoup

import logging.handlers

log = logging.getLogger('coogie')
log.setLevel(logging.INFO)
formatter = logging.Formatter(
    '[%(levelname)s] (%(filename)s:%(lineno)d) > %(message)s')

fileHandler = logging.FileHandler('/home/ubuntu/telebot/log.txt')

fileHandler.setFormatter(formatter)
log.addHandler(fileHandler)

token_ = '1723844569:AAHboDpNc_e6KPGwX_bU7uRXfK_kK0MD9kw'
updater = Updater(token=token_, use_context=True)
now = datetime.now()
dispatcher = updater.dispatcher

flag_ = 0
member = []


def echo(update, context):
    if flag_ == 0:
        if '힘들다' in update.message.text or '졸립다' in update.message.text:
            context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open(
                r'/home/ubuntu/telebot/download.jpg', 'rb'))


def random_(update, context):
    if len(context.args) > 0:
        if context.args[0] == '-m':
            member_list = ""
            for i in member:
                member_list = member_list + i + "\n"
            return context.bot.send_message(chat_id=update.effective_chat.id,
                                            text=member_list)
        elif context.args[0] == '-d':
            member.remove(context.args[1])
            member_list = ""
            for i in member:
                member_list = member_list + i + "\n"
            return context.bot.send_message(chat_id=update.effective_chat.id,
                                            text=member_list)
        elif context.args[0] == '-p':
            member.append(context.args[1])
            print(context.args[1])
            member_list = ""
            for i in member:
                member_list = member_list + i + "\n"
            return context.bot.send_message(chat_id=update.effective_chat.id,
                                            text=member_list)
    context.bot.send_message(chat_id=update.effective_chat.id, text=member[
                                                                        random.randrange(
                                                                            0,
                                                                            4)] + ' 당첨!! 확률 : ' + str(
        100 / len(member)) + '%!')


def photo(update, context):
    temp = ""
    for i in context.args:
        temp = temp + i + " "
    service = build("customsearch", "v1",
                    developerKey='AIzaSyC7PUDhgSLOmMdqHYO1I1qzdJFa2486Q-s')
    result = service.cse().list(
        q=temp,
        cx='5173d767a8e36d1a9',
        num=3,
        searchType='image',
    ).execute()
    atai = random.randrange(0, 3)
    print(result['items'][0])
    context.bot.sendPhoto(chat_id=update.effective_chat.id,
                          photo=result['items'][atai]['link'])
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=result['items'][atai]['image']['contextLink'])
    print(result['items'][0]['link'])
    print(temp)


def date_cal(update, context):
    try:
        if type(context.args[1]) == str:
            print("문자열", context.args[1])
    except IndexError:
        pass
    str_date = datetime.strptime(context.args[0], '%Y%m%d').date()
    days = (date.today() - str_date).days
    per = round(days / 730 * 100)
    if days < 0 :
        context.bot.send_message(chat_id=update.
                                 effective_chat.id, text="잘못된 날짜가 입력됐어요.")
        return
    context.bot.send_message(chat_id=update.
                             effective_chat.id, text="내일채움 "
                                                     "시작일로부터 "
                                                     "" + str(days)
                                                     + "일 지났고, "
                                                       "\n" +
                                                     str(per)
                                                     + " % "
                                                       "완료하였습니다.")


def stock(update, context):
    URL = "https://www.google.com/search?q={query}+주가".format(
        query=context.args[0])
    soup = BeautifulSoup(requests.get(URL).content, 'html.parser')
    select = soup.select('.kCrYT')
    split = select[11].getText().split(" ")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=context.args[0] + "의 주식정보입니다.\n" + "현재가 : " + split[0] + " " + split[9] + " " + "전날대비 :" + split[1])


def weather(update, context):
    str_ = "".join(context.args)
    print(str_)
    return context.bot.send_message(chat_id=update.effective_chat.id,
                                    text="저는 일안해요")


def help_(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="🕵️‍이미지 검색   '/p 검색할 이미지' \n"
                                  "📆월급날 계산   '/payday' \n"
                                  "📆내일채움공제   '/date yyyymmdd'\n"
                                  "💰주식조회      '/s 검색할 주식\n"
                                  "😧도움말   '/h'\n"
                             )


def payday(update, context):
    if date.today().day > 25:
        a = date(datetime.today().year,
                 datetime.today().month + 1, 25).weekday()
    else:
        a = date(datetime.today().year,
                 datetime.today().month, 25).weekday()
    if a == 6:
        b = 25 - 2
    elif a == 5:
        b = 25 - 1
    else:
        b = 25
    month_day = date(datetime.today().year,
                     datetime.today().month,
                     datetime.today().day)
    if date.today().day > b:
        result = date(datetime.today().year,
                      datetime.today().month + 1,
                      b) - month_day
    else:
        result = date(datetime.today().year, datetime.today().month,
                      b) - month_day
    if date.today().day > b:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=str(datetime.today().month + 1) + '월은 ' +
                                  str(b) + '일이 월급날입니다\n''월급까지 ' +
                                  str(result.days) + "일 남았습니다.")
    else:
        if int(result.days) == 1:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='월급까지 하루 남았습니다!!\n'
                                          '소리질뤄ㅓㅓㅓㅓㅓ~~~~'
                                     )
            context.bot.sendAnimation(chat_id=update.effective_chat.id,
                                      animation=open(
                                          r'/home/ubuntu/telebot/1.gif', 'rb'))
            context.bot.sendAnimation(chat_id=update.effective_chat.id,
                                      animation=open(
                                          r'/home/ubuntu/telebot/2.gif', 'rb'))
            return 0
        elif int(result.days) == 0:
            context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open(
                r'/home/ubuntu/telebot/payday.png', 'rb'))
            return 0
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=str(datetime.today().month) + '월은 ' +
                                  str(b) + '일이 월급날입니다\n''월급까지 ' +
                                  str(result.days) + "일 남았습니다.")


def main():
    try:
        weather_handler = CommandHandler('w', weather)
        photo_handler = CommandHandler('p', photo)
        date_handler = CommandHandler('date', date_cal)
        help_handler = CommandHandler('h', help_)
        random_handler = CommandHandler('random', random_)
        payday_handler = CommandHandler('payday', payday)
        stock_handler = CommandHandler('s', stock)
        echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
        dispatcher.add_handler(echo_handler)
        dispatcher.add_handler(photo_handler)
        dispatcher.add_handler(help_handler)
        dispatcher.add_handler(date_handler)
        dispatcher.add_handler(weather_handler)
        dispatcher.add_handler(random_handler)
        dispatcher.add_handler(payday_handler)
        dispatcher.add_handler(stock_handler)
        updater.start_polling()
        updater.idle()
    except Exception as e:
        log.warning(e)


if __name__ == '__main__':
    main()
