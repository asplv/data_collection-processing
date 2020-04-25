# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']

    def __init__(self, text):
        self.start_urls = [
            f'https://russia.superjob.ru/vacancy/search/?keywords={text}']

    def parse(self, response):
        next_page = response.xpath("//a[@class = 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href").extract_first()

        vacancy_links = response.xpath("//div[@class = '_3mfro CuJz5 PlM3e _2JVkc _3LJqf']/a/@href").extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)

        yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        url = response.url
        title = response.xpath("//h1[@class = '_3mfro rFbjy s1nFK _2JVkc']/text()").extract_first()
        salary = response.xpath("//span[@class = '_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()").extract()
        employer = response.xpath("//div[@class = '_3zucV undefined']//h2[@class = '_3mfro PlM3e _2JVkc _2VHxz _3LJqf _15msI']/text()").extract_first()
        yield JobparserItem(url=url, title=title, employer=employer, salary=salary)





