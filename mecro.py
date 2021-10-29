from selenium import webdriver as wd
import chromedriver_autoinstaller
import time
import pymysql
import os

def clearConsole():
    command = 'cls'
    os.system(command)

db = pymysql.connect(
    host="localhost",
    user="root",
    passwd="NamchunSQL!@",
    database="project",
    autocommit='TRUE')
mycursor = db.cursor(pymysql.cursors.DictCursor)

coin_list = ('BTC', 'ETH', 'XRP', 'DOGE', 'EOS', 'ETC', 'BTT', 'XLM')
coins = {}
old_const = {}

path = chromedriver_autoinstaller.install()
driver = wd.Chrome(path)
driver.maximize_window()

# 전일가 가져오기
for coin in coin_list:
    driver.get(f"https://www.bithumb.com/trade/order/{coin}_KRW")
    driver.implicitly_wait(5); driver.set_page_load_timeout(5)
    old_const[coin] = driver.find_element_by_xpath('//span[@id="contBeforeDayLast"]').text.replace(',', '')
    mycursor.execute(f"UPDATE coins SET old_const = '{old_const[coin]}' WHERE coin_name = '{coin}'")
    db.commit()

# 현재가 가져오기
while True:
    for coin in coin_list:
        coins[coin] = driver.find_element_by_id(f"assetReal{coin}_KRW").text.replace(',', '')
        percent = driver.find_element_by_id(f"assetRealRate{coin}_KRW").text.replace('%', '')
        mycursor.execute(f"UPDATE coins SET const = {coins[coin]}, percent = {percent} WHERE coin_name = '{coin}'")
        db.commit()

    clearConsole()
    time.sleep(1)

driver.close()
driver.quit()