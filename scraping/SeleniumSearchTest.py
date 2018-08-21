# さっきpip install seleniumで入れたseleniumのwebdriverというやつを使う
from selenium import webdriver
# さっきDLしたchromedriver.exeを使う
driver = webdriver.Chrome("C:/Vagrant/share/driver/chromedriver.exe")

# chrome起動してyahooに移動
driver.get("http://www.yahoo.co.jp/")

#検索入力ボックスのhtmlを探す
searchBox = driver.find_element_by_css_selector("#srchtxt")

#その検索ボックスで　「世の中 憎い」と入力
searchBox.send_keys("猛暑")

#htmlから検索ボタンを探す
kensakuBotan = driver.find_element_by_css_selector("#srchbtn")

#検索ボタンをクリック
kensakuBotan.click()