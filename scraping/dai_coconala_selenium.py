# from selenium import webdriver
# driver = webdriver.Chrome("C:/Vagrant/share/driver/chromedriver.exe")
# driver.get("http://www.yahoo.co.jp")

import sys
import os
from selenium import webdriver
import pandas
import time

browser = webdriver.Chrome(executable_path='C:/Vagrant/share/driver/chromedriver.exe')

#1

args = sys.argv
df = pandas.DataFrame()
# df = pandas.read_csv('C:/Vagrant/share/scraping/default.csv' , index_col=0)
# df = pandas.read_csv('default.csv', index_col=0)

#3

browser.get("https://coconala.com/categories/176")

#4

page = 1

#5

while True: #continue until getting the last page

    #5-1

    if len(browser.find_elements_by_css_selector("a.next")) > 0:
        print("######################page: {} ########################".format(page))
        print("Starting to get posts...")

        #5-1-2

        time.sleep(5)

        posts = browser.find_elements_by_css_selector(".listContentBox") #ページ内のタイトル複数
        print (len(posts))

        #5-1-3

        for post in posts:

            try:

                title = post.find_element_by_css_selector("a.js-service-view-tracker").text
                print(title)

                detail = post.find_element_by_css_selector("h3").text
                print(detail)

                #5-1-3-1

                price = post.find_element_by_css_selector("strong.red").text
                print(price)
                #5-1-3-2

                liked = post.find_element_by_css_selector("span.overlay").text
                print(liked)

                url = post.find_element_by_css_selector("a.js-service-view-tracker").get_attribute("href")
                se = pandas.Series([title,detail, price, liked,url],index=['title', 'detail','price','liked','url'])
                df = df.append(se, ignore_index=True)
            except:
                print("Error:Advertisement appeared.Skipping...")

        #5-1-4

        page+=1

        btn = browser.find_element_by_css_selector("a.next").get_attribute("href")
        print("next url:{}".format(btn))
        browser.get(btn)
        print("Moving to next page......")

    #5-2

    else:
        print("no pager exist anymore")
        break
#6
print("Finished Scraping. Writing CSV.......")
df.to_csv("C:/Vagrant/share/scraping/coconalaoutput.csv")
print("DONE")