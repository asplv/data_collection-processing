# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from functools import partial


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']

    def __init__(self, text):
        self.start_urls = [
            f'https://hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text={text}&showClusters=false']

    def parse(self, response: HtmlResponse):
        vacancy_links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").extract()
        for link in vacancy_links:
            yield response.follow(link, callback=partial(self.vacancy_parse, link=link))

        next_page = response.xpath("//a[@data-qa = 'pager-next']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse, link):
        url = link
        title = response.xpath("//div[@class = 'vacancy-title']/h1//text() | "
                               "//div[@class = 'vacancy-title ']/h1/text()").extract_first()
        salary = response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract()
        employer = response.xpath("//a[@data-qa = 'vacancy-company-name']/span/text()").extract()
        source = self.allowed_domains[0]
        yield JobparserItem(url=url, title=title, employer=employer, source=source, salary=salary)





