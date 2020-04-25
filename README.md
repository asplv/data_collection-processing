# data_collection-processing

This repository contains practice of data collection and processing tools using python

1. - Parsing Github API to get list of repos by user.
   - Authentication to Oxford Dictionaries API https://developer.oxforddictionaries.com/ and getting basic entry.
   - Recieving VK API https://vk.com/dev/first_guide token and applying a method.

2. Parsing job search sites - hh.ru https://hh.ru/ and superjob https://russia.superjob.ru/. Extracting the most essential information about vacancies.

3. Adding results of job parser to MongoDB collection. Some enhancements: 
- prevention from data re-writing after another launch of the parser;
- filtration by salary.

4. Parsing large russian news aggregators using xpath:
- News.mail.ru https://news.mail.ru/
- Yandex.news https://yandex.ru/news/
- Lenta.ru https://lenta.ru/

5. Implementing jobparser by scrapy basing on hh.ru https://hh.ru/ and superjob https://russia.superjob.ru/

6. Parsing online store https://leroymerlin.ru/
- Collecting url, title, price, features and all-size photos