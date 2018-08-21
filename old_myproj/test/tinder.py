# coding: UTF-8
import os
import time
import random
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
chrome = webdriver.Chrome('./chromedriver')
chrome.get("https://tinder.com/app/login")
val = input('ログイン後、0を押してください')
max_count = 500
if val == 0:
    for num in range(1,max_count):
        num=num+1
        chrome.find_element_by_tag_name("body").send_keys(Keys.RIGHT)
        time.sleep(0.3)
        print(str(num))
    print(str(max_count)+"人スワイプしました")
    chrome.close()