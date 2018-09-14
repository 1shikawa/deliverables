# https://qiita.com/Brutus/items/0a2e8d0c682d10c65a03

# スクレイピングに必要なモジュールをインポート
import urllib.request as req
import sys
from bs4 import BeautifulSoup

# Messaging APIのモジュールをインポート
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

# channel access tokenを指定
line_bot_api = LineBotApi('ubTztMRCsDJCJy/EtDIiip+K5/n3GO7hHkIioCvN/Bx0GW3fsn0MKiZiiAQzoSwq6iv7hN8QjsLkPLtVcKAGubxLNT3Uxw7VEgyWi1X5hlhjaYOvo2ovc8deBTTCa8TP/xC8ue5ASeaVvZ5zY15TAQdB04t89/1O/w1cDnyilFU=')

# user IDとプッシュメッセージを指定
def message1():
        try:
            line_bot_api.push_message('U46574d1b32f3eef2619b921c17f27998', TextSendMessage(text=str(train) + ":" + str(status) + "   " + str(info)))
        except LineBotApiError as e:
        # error handle
          print("Error occurred")

url = "https://transit.yahoo.co.jp/traininfo/detail/21/0/"
res = req.urlopen(url)
soup = BeautifulSoup(res, "lxml")

train = soup.select_one("#main > div.mainWrp > div.labelLarge > h1").text
print(train)
status = soup.select_one("#mdServiceStatus > dl > dt").text
print(status)

if not status == "[○]平常運転":
    info = soup.select_one("#mdServiceStatus > dl > dd > p").text
    print(info)
    message1()