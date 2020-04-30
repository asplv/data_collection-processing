# Программа, реализующая сбор входящих писем из почтового ящика и складывающая данные о них в базу данных

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo import MongoClient
import time

driver = webdriver.Chrome()
driver.get('https://m.mail.ru/login')
assert "Mail.Ru" in driver.title
time.sleep(1)

# авторизация
elem = driver.find_element_by_name('Login')
elem.send_keys('study.ai_172@mail.ru')
elem = driver.find_element_by_name('Password')
elem.send_keys('NewPassword172')
elem.send_keys(Keys.RETURN)

# извлекаем количество страниц
pages_count = driver.find_element_by_xpath("//td[@class = 'pager__list__item'][position()=last()] ").text
links = []

# собираем ссылки со всех страниц
for i in range(int(pages_count)):
    if i != 0:
        # нажимаем кнопку далее
        page_arrow = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//a[@title='Следующая страница']"))
            )
        page_arrow.send_keys(Keys.RETURN)

    elements = driver.find_elements_by_class_name('messageline__link')
    for elem in elements:
        link = elem.get_attribute('href')
        links.append(link)


client = MongoClient('localhost', 27017)
db = client['mail_parser_db']
mail_ru = db.mail_ru

# собираем информацию о письме
for link in links:
    letter_data = {}
    letter = driver.get(link)
    letter_data['_id'] = link[-20:]
    letter_data['addresser'] = driver.find_element_by_class_name('readmsg__text-container__inner-line').text
    letter_data['date'] = driver.find_element_by_class_name('readmsg__mail-date').text
    letter_data['theme'] = driver.find_element_by_class_name('readmsg__theme').text
    letter_data['body'] = driver.find_element_by_id('readmsg__body').text

    # проверяем уникальность по id
    obj = next(mail_ru.find({"_id": {'$eq': letter_data['_id']}}), None)
    if not obj:
        mail_ru.insert_one(letter_data)
    else:
        mail_ru.update_one({"_id": {'$eq': letter_data['_id']}}, {'$set': letter_data})
