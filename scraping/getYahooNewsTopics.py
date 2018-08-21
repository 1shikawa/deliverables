# https://qiita.com/Atupon0302/items/352811a2d92d6ebab8c2
# pythonでさくっとスクレイピング（Requests + Beautiful Soup 4）

import  requests
from bs4 import BeautifulSoup
import re

#初回のみ
target_url = "https://www.yahoo.co.jp/"

#Requestsを使って、webから取得
r = requests.get(target_url)

#要素を抽出
soup = BeautifulSoup(r.text,'lxml')

#HTMLファイルとして保存したい場合はファイルオープンして保存
with open('originDataOld.html',mode='w',encoding = 'utf-8') as fw:
    fw.write(soup.prettify()) # prettifyで整形されたファイルで保存
#soup.find_allを用いてリンク先が「news.yahoo.co.jp/pickup」の項目を全て取得
elems = soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))

for e in elems:
    print(e.getText())