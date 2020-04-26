# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Compose
import re


def feature_cleaner(values):
    return values.replace('\n', '').strip()


def feauture_extractor(values):
    return {feature_cleaner(values[i]): feature_cleaner(values[i + 1])
            for i in range(0, len(values), 2)}


def article_extractor(value):
    article_pattern = re.compile(r'\d+')
    article = article_pattern.findall(value[0])
    return article


def price_transform(value):
    price = int(value[0].replace(' ', ''))
    return price


class LeroymerlinparserItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    article = scrapy.Field(output_processor=TakeFirst(), input_processor=Compose(article_extractor))
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=Compose(price_transform))
    url = scrapy.Field(output_processor=TakeFirst())
    features = scrapy.Field(input_processor=Compose(feauture_extractor))
    photos = scrapy.Field()
