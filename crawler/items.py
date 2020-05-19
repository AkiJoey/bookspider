# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    isbn = scrapy.Field()
    cover = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    press = scrapy.Field()
    date = scrapy.Field()
    page = scrapy.Field()
    summary = scrapy.Field()
    
    pass
