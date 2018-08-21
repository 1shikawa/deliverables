# encoding: utf-8
# https://qiita.com/drumvicfirth/items/4cfc9cb54fdbc53824bb
# Python3+Beautifulsoup+Requestsで画像収集&クエリーパラメータ操作
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import os
import sys

def download_site_images(url,path,query):
    images = []

    if not os.path.exists(path):
        os.makedirs(path)

    url = requests.get(url,params=query)

    soup = BeautifulSoup(url.content,'lxml')

    for link in soup.find_all("img"):
        src = link.get("src")

        if 'jpg' in src:
            images.append(src)
        elif 'png' in src:
            images.append(src)
        elif 'gif' in src:
            images.append(src)

    for image in images:
        re = requests.get(image)
        print('Downloading:',image)
        with open(path + image.split('/')[-1],'wb') as f:
            f.write(re.content)


def get_url():
    response = input("plz paste the url what you want to crawl\n")
    return response

def get_now_time():
    now_time = datetime.now().strftime("%Y_%m_%d")
    return now_time

def get_query():
    query = []
    params = []
    flg = int(input("do you want to input any query?\nyes = 1,no = 0\n"))

    while(flg == 1):
        key = input("plz input words of query key\n")

        query.append(key)
        val = input("plz input words of query value\n")
        val = val.replace(" ","+")
        params.append(val)

        flg = int(input("do you want to continue inputting query?\nyes = 1,no = 0\n"))

    dic = dict(zip(query,params))

    return dic



if __name__ == '__main__':
    flg = 1
    while(flg == 1):
        url = get_url()
        now_time = get_now_time()
        query = get_query()
        download_site_images(url,f'img/{now_time}',query)

        flg = int(input("do you want to continue crawling?\nyes = 1,no = 0\n"))