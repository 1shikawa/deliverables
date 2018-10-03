# https://qiita.com/trung_vs/items/f71ecb44e83b7c3b89d3

import requests
from bs4 import BeautifulSoup
Fanza = requests.get('http://www.dmm.co.jp/digital/videoa/-/ranking/=/type=actress//')
soup = BeautifulSoup(Fanza.text,'html.parser')
joyu_list = soup.find_all('div', class_='data')
rank = 1
print('月間 AV女優ランキング ベスト20')
for joyu in joyu_list:
    print(str(rank) + "位:" + joyu.a.get_text())
    rank += 1