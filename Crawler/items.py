# -*- coding: utf-8 -*-
import scrapy


class PageItem(scrapy.Item):
    """docstring for ArticleItem"""
    site = scrapy.Field()
    keyword = scrapy.Field()
    reprints = scrapy.Field()
    titles = scrapy.Field()
    descriptions = scrapy.Field()
    hints = scrapy.Field()
    publishs = scrapy.Field()
    newspapers = scrapy.Field()
    counties = scrapy.Field()
    types = scrapy.Field()
    words = scrapy.Field()
    pages = scrapy.Field()
    tags = scrapy.Field()
    ocrs = scrapy.Field()
    download_pages = scrapy.Field()
    download_urls = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    search_id = scrapy.Field()