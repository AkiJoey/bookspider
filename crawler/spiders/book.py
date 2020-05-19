# -*- coding: utf-8 -*-
import scrapy

from crawler.items import BookItem

class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['douban.com']
    start_urls = ['https://book.douban.com/subject/25985021/']

    def parse(self, response):
        item = BookItem()

        item['isbn'] = getField(response.xpath(u'//span[contains(./text(), "ISBN:")]/following::text()[1]').extract_first())
        item['title'] = getField(response.css('#wrapper > h1 > span::text').extract_first())
        item['cover'] = getField(response.css('#mainpic > a > img::attr(src)').extract_first())
        item['author'] = getAuthor(response)
        item['press'] = getField(response.xpath(u'//span[contains(./text(), "出版社:")]/following::text()[1]').extract_first())
        item['date'] = getField(response.xpath(u'//span[contains(./text(), "出版年:")]/following::text()[1]').extract_first())
        item['page'] = getField(response.xpath(u'//span[contains(./text(), "页数:")]/following::text()[1]').extract_first())
        item['summary'] = getSummary(response)

        yield item

        likes = response.css('#db-rec-section > div > dl')
        for like in likes:
            like_url = like.css('dt > a::attr(href)').extract_first()
            if like_url:
                yield scrapy.Request(url = like_url, callback = self.parse)

def getField(field):
    return field.strip()

def getAuthor(response):
    author = response.css('#info > a:nth-child(2)::text').extract_first()
    if not author:
        author = response.css('#info > span > a::text').extract_first()
    return author.replace('\n            ', '').strip()

def getSummary(response):
    section = response.css('#link-report > div:nth-child(1) > div > p::text').extract()
    summary = ''
    for s in section:
        summary += '\n' + s.strip()
    return summary.strip() if summary else None
