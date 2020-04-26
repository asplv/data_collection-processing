# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import os


class LeroymerlinparserPipeline(object):

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroymerlin

    def process_item(self, item, spider):
        # характеристики
        if item['features']:
            item['features'] = item['features'][0]

        # пополнение базы
        collection = self.mongo_base[spider.name]
        obj = next(collection.find({"url": {'$eq': item['url']}}), None)
        if not obj:
            collection.insert_one(item)
        else:
            collection.update_one({"url": {'$eq': item['url']}}, {'$set': item})
        return item


class LeroymerlinPhotosPipeline(ImagesPipeline):

    def extract_filename(self, url):
        # извлекаем название файла из ссылки
        prefix = url[url.find('upload/') + 7:]
        prefix = prefix[:prefix.find('/')]

        filename = url[url.rfind('/') + 1:]
        return prefix + '_' + filename

    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                filename = self.extract_filename(img)
                try:
                    yield scrapy.Request(img, flags=[item['article'], filename])
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None):
        return os.path.join(request.flags[0], request.flags[1])


