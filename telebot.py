from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import random
from googleapiclient.discovery import build
import yaml
import pyautogui
from selenium import webdriver
import time

with open('key.yml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
token_ = data['key']['telegram']['token']
updater = Updater(token=token_, use_context=True)
dispatcher = updater.dispatcher


def echo(update, context):
    if '술' in update.message.text:
        text = ['저요', '나요', 'me', 'わたし！']
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text[random.randrange(0, 4)])


def photo(update, context):
    temp = context.args
    service = build("customsearch", "v1",
                    developerKey=data['key']['google']['key'])
    result = service.cse().list(
        q=temp[0],
        cx=data['key']['google']['cx'],
        num=1,
        searchType='image',
    ).execute()
    context.bot.sendPhoto(chat_id=update.effective_chat.id,
                          photo=result['items'][0]['link'])
    print(result['items'][0]['link'])
    print(temp)


def weather(update, context):
    str_ = "".join(context.args)
    print(str_)
    if '날씨' in str_:
        url = f'https://search.naver.com/search.naver?query=%s' % str_
        driver = webdriver.Chrome('./chromedriver')
        driver.get(url)
        time.sleep(3)
        pyautogui.screenshot("./today.png", region=(60, 420, 675, 375))
        driver.quit()
        context.bot.sendPhoto(chat_id=update.effective_chat.id,
                              photo=open(
                                  '/Users/myeongkookpark/PycharmProjects'
                                  '/coogie_bot/today.png',
                                  'rb'))
        print(context.args)
    else:
        return context.bot.send_message(chat_id=update.effective_chat.id,
                                        text="~날씨로 검색해주세요\n"
                                             "예: 내일 강남구 날씨, 다음주 날씨")


def help_(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="1.이미지 검색   '/p 검색할 이미지' \n"
                                  "2.날씨 검색   '/w 지역+날씨 \n"
                                  "3.도움말   '/h'\n")


def main():
    weather_handler = CommandHandler('w', weather)
    photo_handler = CommandHandler('p', photo)
    help_handler = CommandHandler('h', help_)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(photo_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(weather_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
