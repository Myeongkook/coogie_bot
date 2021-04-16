import re
import time
import yaml
import random
import pyautogui
from datetime import date
from selenium import webdriver
from googleapiclient.discovery import build
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

with open('key.yml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
token_ = data['key']['telegram']['token']
updater = Updater(token=token_, use_context=True)
dispatcher = updater.dispatcher

flag_ = 0
member = ['교봉주임님', '수연주임님', '상민주임님', '명국주임님']


def echo(update, context):
    if flag_ == 0:
        if '힘들다' in update.message.text or '졸립다' in update.message.text:
            context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open(r'C:\Users\Myeongkook Park\PycharmProjects\TestPython\telebot\download.jpg', 'rb'))
        elif update.message.text == '쿠기야 조용해':
            print(flag_)
            context.bot.send_message(chat_id=update.effective_chat.id, text='네...')


def random_(update, context):
    if len(context.args) > 0:
        if context.args[0] == '-m':
            member_list = ""
            for i in member:
                member_list = member_list + i + "\n"
            return context.bot.send_message(chat_id=update.effective_chat.id, text=member_list)
        elif context.args[0] == '-d':
            member.remove(context.args[1])
            print(context.args[1])
            member_list = ""
            for i in member:
                member_list = member_list + i + "\n"
            return context.bot.send_message(chat_id=update.effective_chat.id, text=member_list)
        elif context.args[0] == '-p':
            member.append(context.args[1])
            print(context.args[1])
            member_list = ""
            for i in member:
                member_list = member_list + i + "\n"
            return context.bot.send_message(chat_id=update.effective_chat.id, text=member_list)
    context.bot.send_message(chat_id=update.effective_chat.id, text=member[random.randrange(0, 4)] + ' 당첨!! 확률 : ' + str(100 / len(member)) + '%!')


def photo(update, context):
    temp = ""
    for i in context.args:
        temp = temp + i + " "
    service = build("customsearch", "v1",
                    developerKey=data['key']['google']['key'])
    result = service.cse().list(
        q=temp,
        cx=data['key']['google']['cx'],
        num=5,
        searchType='image',
    ).execute()
    atai = random.randrange(0, 5)
    print(result['items'][0])
    context.bot.sendPhoto(chat_id=update.effective_chat.id,
                          photo=result['items'][atai]['link'])
    context.bot.send_message(chat_id=update.effective_chat.id, text=result['items'][atai]['image']['contextLink'])
    print(result['items'][0]['link'])
    print(temp)


def date_cal(update, context):
    try:
        if type(context.args[1]) == str:
            print("문자열", context.args[1])
    except IndexError:
        pass
    start = date(int(context.args[0][0:4]), int(context.args[0][5:6]),
                 int(context.args[0][6:8]))
    days = (date.today() - start).days
    per = round(days / 730 * 100)
    context.bot.send_message(chat_id=update.
                             effective_chat.id, text="내일채움 "
                                                     "시작일로 부터 "
                                                     "" + str(days)
                                                     + "일 지났고, "
                                                       "\n" +
                                                     str(per)
                                                     + " % "
                                                       "완료하였습니다.")


def weather(update, context):
    str_ = "".join(context.args)
    print(str_)
    # if '날씨' in str_:
    #     url = f'https://search.naver.com/search.naver?query=%s' % str_
    #     driver = webdriver.Chrome('./chromedriver.exe')
    #     driver.get(url)
    #     time.sleep(3)
    #     pyautogui.screenshot("./today.png", region=(50, 390, 675, 375))
    #     driver.quit()
    #     context.bot.sendPhoto(chat_id=update.effective_chat.id,
    #                           photo=open(
    #                               r'C:\Users\Myeongkook Park\PycharmProjects\TestPython\telebot\today.png',
    #                               'rb'))
    # else:
    return context.bot.send_message(chat_id=update.effective_chat.id,
                                        text="저는 일안해요")


def help_(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="🕵️‍이미지 검색   '/p 검색할 이미지' \n"
                                  "📆내일채움공제   '/date yyyymmdd'\n"
                                  "😧도움말   '/h'\n"
                                  )


def main():
    weather_handler = CommandHandler('w', weather)
    photo_handler = CommandHandler('p', photo)
    date_handler = CommandHandler('date', date_cal)
    help_handler = CommandHandler('h', help_)
    random_handler = CommandHandler('random', random_)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(photo_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(date_handler)
    dispatcher.add_handler(weather_handler)
    dispatcher.add_handler(random_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
