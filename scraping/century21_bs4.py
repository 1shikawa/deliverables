# https://qiita.com/oppasiri330/items/0f9526a1c507ae170a56
import requests
from bs4 import BeautifulSoup

r = requests.get('https://pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/')
soup = BeautifulSoup(r.content,'html.parser')

#page数の取得
page_nr=soup.find_all("a",{"class":"Page"})[-1].text

base_url="https://pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="

l = []
for page in range(0, int(page_nr)*10, 10):
    url=base_url+str(page)+".html"
    print(url)
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("div", {"class":"propertyRow"})#class=valueなどは辞書で渡す{}

for item in all:
    d = {}

    price = item.find_all("h4", {"class", "propPrice"})[0].text.replace("\n", "")
    d["Price"] = price

    address = item.find_all("span", {"class": "propAddressCollapse"})
    try:
        d["Address"] = address[0].text
    except:
        d["Address"] = None
    try:
        d["Locality"] = address[1].text
    except:
        d["Locality"] = None

    l.append(d)

import pandas as pd
#除書のリストからデータフレーム作成
df = pd.DataFrame(l)
df.to_csv("century21.csv")