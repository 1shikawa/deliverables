# https://qiita.com/Azunyan1111/items/b161b998790b1db2ff7a

# coding: UTF-8
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions() # ブラウザのオプションを格納する変数をもらってきます。
# options.binary_location = "./bin/headless-chromium"
options.add_argument("--headless") # Headlessモードを有効にする
options.add_argument("--no-sandbox")
options.add_argument("--single-process")

# ブラウザを起動する
driver = webdriver.Chrome(
    executable_path="/home/vagrant/bin/chromedriver",
    chrome_options=options
)

# ブラウザでアクセスする
driver.get("https://www.light-weight-baby.net/")

# HTMLを文字コードをUTF-8に変換してから取得します。
html = driver.page_source.encode('utf-8')

# BeautifulSoupで扱えるようにパースします
soup = BeautifulSoup(html, "html.parser")

# idがheikinの要素を表示
print(soup.select_one("div.header-info"))