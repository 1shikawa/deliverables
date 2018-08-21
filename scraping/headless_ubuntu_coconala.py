# https://qiita.com/mc-chinju/items/9fcfc70e7b6156312cfe
from selenium import webdriver
import time
import pandas
import sys

options = webdriver.ChromeOptions()
# options.binary_location = "./bin/headless-chromium"
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--single-process")

driver = webdriver.Chrome(
    executable_path="/home/vagrant/bin/chromedriver",
    chrome_options=options
)

args = sys.argv
df = pandas.read_csv('/home/vagrant/share/scraping/default.csv' , index_col=0)


driver.get("https://coconala.com/categories/176")

page = 1

#5

while True: #continue until getting the last page

    #5-1

    if len(driver.find_elements_by_css_selector("a.next")) > 0:
        print("######################page: {} ########################".format(page))
        print("Starting to get posts...")

        #5-1-2

        time.sleep(5)

        posts = driver.find_elements_by_css_selector(".listContentBox") #ページ内のタイトル複数
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
                se = pandas.Series([title,detail, price, liked,url],['title', 'detail','price','liked','url'])
                # df = df.append(se, ignore_index=True)
            except:
                print("Error:Advertisement appeared.Skipping...")

        #5-1-4

        page+=1

        btn = driver.find_element_by_css_selector("a.next").get_attribute("href")
        print("next url:{}".format(btn))
        driver.get(btn)
        print("Moving to next page......")

    #5-2

    else:
        print("no pager exist anymore")
        break
#6
print("Finished Scraping. Writing CSV.......")
df.to_csv("/home/vagrant/share/scraping/headless_output.csv")
print("DONE")