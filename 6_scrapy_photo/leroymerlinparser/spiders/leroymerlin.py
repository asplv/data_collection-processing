# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leroymerlinparser.items import LeroymerlinparserItem


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, text):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={text}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='paginator-button next-paginator-button']/@href").extract_first()

        item_links = response.xpath("//div[@class='ui-product-card']/@data-product-url").extract()
        for link in item_links:
            yield response.follow(link, callback=self.parse_items)

        yield response.follow(next_page, callback=self.parse)

    def parse_items(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinparserItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_xpath('title', "//h1[@slot='title']/text()")
        loader.add_xpath('article', "//span[@slot='article']/text()")
        loader.add_xpath('price', "//uc-pdp-price-view[@class='primary-price']/span[@slot='price']/text()")
        loader.add_xpath('photos', "//source[@itemprop='image']/@srcset")
        loader.add_xpath('features', "//dt[@class='def-list__term']/text() | //dd[@class='def-list__definition']/text()")
        yield loader.load_item()


