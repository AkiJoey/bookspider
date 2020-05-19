# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import pymysql
from scrapy.exceptions import DropItem

from crawler.items import BookItem
from crawler.utils import RedisUtil

class DuplicatePipeline(object):
    def __init__(self):
        self.redisUtil = RedisUtil()
 
    def process_item(self, item, spider):
        if self.redisUtil.exist(item['isbn']):
            raise DropItem(item['title'] + ' is already crawled')
        else:
            self.redisUtil.save(item['isbn'])
            return item

class InsertPipeline(object):
    def __init__(self):
        self.connection = pymysql.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            passwd = 'root',
            db = 'library'
        )
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        insert = 'insert into book(isbn, cover, title, author, press, date, page, summary) values (%s, %s, %s, %s, %s, %s, %s, %s)'
        if isinstance(item, BookItem):
            values = (item['isbn'], item['cover'], item['title'], item['author'], item['press'], item['date'], item['page'], item['summary'])
            self.cursor.execute(insert, values)
            self.connection.commit()
        return item
