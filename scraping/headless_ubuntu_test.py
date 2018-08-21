# https://qiita.com/mc-chinju/items/9fcfc70e7b6156312cfe
from selenium import webdriver

options = webdriver.ChromeOptions()
# options.binary_location = "./bin/headless-chromium"
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--single-process")

driver = webdriver.Chrome(
    executable_path="/home/vagrant/bin/chromedriver",
    chrome_options=options
)

driver.get("https://coconala.com/categories/176")
print(driver.title)


# https://qiita.com/nbeat/items/4b915677e1d4e9e21ca2
# UbuntuのCLI環境でGoogleChromeを使ってウェブサイトのスクリーンショットを取得する
# from selenium import webdriver
# from pyvirtualdisplay import Display
#
# display = Display(visible=0, size=(1024, 768))
# display.start()
#
# driver = webdriver.Chrome()
# driver.set_window_size(1024, 768)
#
# driver.get('https://www.google.com')
#
# driver.save_screenshot("screenshot.png")
#
# driver.quit()
# display.stop()