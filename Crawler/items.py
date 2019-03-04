# -*- coding: utf-8 -*-
import scrapy
import json


class PageItem(scrapy.Item):
    site = scrapy.Field()
    keyword = scrapy.Field()
    reprint = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    hint = scrapy.Field()
    publish = scrapy.Field()
    newspaper = scrapy.Field()
    county = scrapy.Field()
    type = scrapy.Field()
    word = scrapy.Field()
    page = scrapy.Field()
    tag = scrapy.Field()
    ocr = scrapy.Field()
    download_page = scrapy.Field()
    download_url = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    search_id = scrapy.Field()
    generate_json = scrapy.Field()


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    hint = scrapy.Field()
    publish = scrapy.Field()
    newspaper = scrapy.Field()
    county = scrapy.Field()
    type_ = scrapy.Field()
    word = scrapy.Field()
    page = scrapy.Field()
    tag = scrapy.Field()
    site = scrapy.Field()
    reprint = scrapy.Field()
    download_page = scrapy.Field()
    download_url = scrapy.Field()
    ocr = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    search_id = scrapy.Field()

