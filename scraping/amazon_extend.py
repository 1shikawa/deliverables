import sys
import os
from selenium import webdriver
import pandas as pd
import time

args = sys.argv
df = pd.DataFrame()

browser = webdriver.Chrome(executable_path='C:/Vagrant/share/driver/chromedriver.exe')
browser.get("https://www.amazon.co.jp/s/ref=nb_sb_noss_2?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Daps&field-keywords=extend")

page = 1
print("######################page: {} ########################".format(page))
print("Starting to get posts...")

time.sleep(2)

posts = browser.find_elements_by_css_selector(".s-item-container")  # ページ内の分割できるコンテンツ
print(len(posts))  # コンテンツ数

# for post in posts:
#     # try:
#         price = post.find_element_by_css_selector("a.a-link-normal a-text-normal").text
#         print(price)
#
#                 price = post.find_element_by_css_selector("span.c-media__job-number").text
#                 print(price)
#
#                 limit = post.find_element_by_css_selector("span.c-media__job-time").text
#                 print(limit)
#
#                 detail_url = post.find_element_by_css_selector("a.c-media__title").get_attribute("href")
#                 print(detail_url)
#
#                 se = pd.Series([price,limit,detail_url],index = ['price','limit','detail_url'])
#                 df = df.append(se, ignore_index=True)
#             except:
#                 print("Error:Advertisement appeared.Skipping...")
#
#         page+=1
#
#         btn = browser.find_element_by_css_selector("a.pager__item__anchor").get_attribute("href") #"次へ"リンク取得
#         print("next url:{}".format(btn))
#         browser.get(btn)
#         print("Moving to next page......")
#     else:
#         print("no pager exist anymore")
#         break
#
# print("Finished Scraping. Writing CSV.......")
# df.to_csv("C:/Vagrant/share/scraping/ranceroutput.csv")
# print("DONE")