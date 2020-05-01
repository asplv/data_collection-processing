# Программа, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import time
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['mvideo_parser_db']
sale_hits = db.sale_hits

# задаем настройки
options = Options()
options.add_argument('start-maximized')
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=options)
driver.get('https://www.mvideo.ru/')
assert "М.Видео - интернет-магазин" in driver.title

# выбираем город
city_button = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//a[@class='btn btn-approve-city']"))
)
city_button.click()

# подсчет страниц в карусели
pages = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "(//div[@data-init='gtm-push-products'])[2]//div[@class='carousel-paging']/a"))
)

for i in range(len(pages)):
    if i != 0:
        next_button = driver.find_element_by_xpath("(//div[@data-init='gtm-push-products'])[2]//a[@class='next-btn sel-hits-button-next']")
        time.sleep(2)
        if 'disabled' in next_button.get_attribute('class'):
            break
        else:
            next_button.send_keys(Keys.RETURN)

    items = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "(//div[@data-init='gtm-push-products'])[2]//li[@class='gallery-list-item']"))
    )


    for item in items:
        item_data = {}
        elem = item.find_element_by_xpath(".//div[@class='c-product-tile-picture__holder']/a")
        item_data['url'] = elem.get_attribute('href')
        item_data['info'] = json.loads(elem.get_attribute('data-product-info'))

        obj = next(sale_hits.find({'info.productId': {'$eq': item_data['info']['productId']}}), None)
        if not obj:
            sale_hits.insert_one(item_data)
        else:
            sale_hits.update_one({'info.productId': {'$eq': item_data['info']['productId']}}, {'$set': item_data})


driver.quit()