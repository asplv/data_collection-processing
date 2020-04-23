# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from jobparser.items import JobparserItem
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sjru import SjruSpider
import re


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.jobsearch

    def process_item(self, item, spider):
        # salary
        item['min_salary'], item['max_salary'], item['currency'] = self.get_salary(item['salary'], spider)
        # удаляем поле c необработанной зп
        del item['salary']
        # employer
        if spider.name == 'hhru':
            item['employer'] = ''.join(item['employer']).replace('\xa0', ' ')
        # пополнение базы
        collection = self.mongo_base[spider.name]
        obj = next(collection.find({"url": {'$eq': item['url']}}), None)
        if not obj:
            collection.insert_one(item)
        else:
            collection.update_one({"url": {'$eq': item['url']}}, {'$set': item})

        return item

    def get_salary(self, salary, spider):
        joined_salary = ' '.join(salary).replace('\xa0', '')
        numbers_in_sal = re.findall('\d+', joined_salary)

        # не указано
        if joined_salary.find('з/п не указана') != -1 or joined_salary.find('По договорённости') != -1:
            min_salary, max_salary, currency = None, None, None
        else:
            # диапазон
            if len(numbers_in_sal) == 2:
                min_salary = int(numbers_in_sal[0])
                max_salary = int(numbers_in_sal[1])
                if spider.name == 'hhru':
                    currency = salary[-2]
                else:
                    currency = salary[-1]
            # от
            elif joined_salary.find('от') != -1:
                min_salary = int(numbers_in_sal[0])
                max_salary = None
                if spider.name == 'hhru':
                    currency = salary[-2]
                else:
                    currency = re.findall('\d+(\w+)', joined_salary)[0]
            # до
            elif joined_salary.find('до') != -1:
                min_salary = None
                max_salary = int(numbers_in_sal[0])
                if spider.name == 'hhru':
                    currency = salary[-2]
                else:
                    currency = re.findall('\d+(\w+)', joined_salary)[0]
            else:
                min_salary = int(numbers_in_sal[0])
                max_salary = min_salary
                currency = re.findall('\d+(\w+)', joined_salary)[0]

        return min_salary, max_salary, currency


