# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Compose


def feature_cleaner(values):
    return values.replace('\n', '').strip()


def feauture_extractor(values):
    return {feature_cleaner(values[i]): feature_cleaner(values[i + 1])
            for i in range(0, len(values), 2)}


class LeroymerlinparserItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    article = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    features = scrapy.Field(input_processor=Compose(feauture_extractor))
    photos = scrapy.Field()
