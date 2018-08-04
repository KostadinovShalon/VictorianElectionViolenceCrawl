# -*- coding: utf-8 -*-
import re
import json
from DB.databasemodels import ArchiveSearchResult
from DB import dbconn, dbutils
import datetime

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class NewsPipeline(object):
    @staticmethod
    def extract_words_from_hints(hints):
        p = re.compile('<[^>]+>')
        return p.sub("", hints)

    @staticmethod
    def extract_words_from_line_break(string_):
        return string_.replace('\n', '').strip()

    @staticmethod
    def extract_number_from_string(str_):
        return re.findall(r"\d+", str_)[0]

    @staticmethod
    def extract_date_from_string(str_):
        return re.sub(r'\s+', '', str_).replace('Published:', '')

    @staticmethod
    def extract_county_from_bracket(str_):
        # s = '(Edinburgh, Scotland),'
        words = re.match(r'.*\((.*)\).*', str_)
        if words is not None:
            return words.group(1)
        else:
            return None

    def process_item(self, page_item, spider):

        if spider.name == 'BNA':
            articles_in_page_count = len(page_item['site'])
            if articles_in_page_count > 0:
                site = page_item['site'][0]
                keyword = page_item['keyword'][0]
                start_date = page_item['start_date'][0]
                end_date = page_item['end_date'][0]
                filename = "{}_{}_{}_{}".format(site, keyword, start_date, end_date)
                for i in range(articles_in_page_count):
                    title = self.extract_words_from_line_break(page_item['titles'][i])
                    description = self.extract_words_from_line_break(page_item['descriptions'][i])
                    hint = self.extract_words_from_hints(page_item['hints'][i])
                    publish = page_item['publishs'][i]
                    newspaper = self.extract_words_from_line_break(page_item['newspapers'][i])
                    county = self.extract_words_from_line_break(page_item['counties'][i])
                    type_ = self.extract_words_from_line_break(page_item['types'][i])
                    word = self.extract_number_from_string(page_item['words'][i])
                    page = self.extract_number_from_string(page_item['pages'][i])
                    tag = self.extract_words_from_line_break(page_item['tags'][i])
                    search_id = page_item['search_id'][i]
                    download_page = page_item['download_pages'][i]
                    download_url = page_item['download_urls'][i]
                    ocr = page_item['ocrs'][i]

                    article_item = ArticleItem(site=site, keyword=keyword, title=title, description=description,
                                               hint=hint, publish=publish, newspaper=newspaper, county=county,
                                               type_=type_, word=word, page=page, tag=tag, download_url=download_url,
                                               download_page=download_page, ocr=ocr, start_date=start_date,
                                               end_date=end_date, search_id=search_id)

                    print 'Writting the data into the json file now..........'
                    article_item.write_into_json_file(filename)
                    article_item.write_into_database()
                dbutils.write_new_search_results(page_item['search_id'][0], filename)

        elif spider.name == 'GN':
            articles_in_page_count = len(page_item['site'])
            for i in range(articles_in_page_count):
                site = page_item['site'][i]
                keyword = page_item['keyword'][i]
                reprint = page_item['reprints'][i]
                title = page_item['titles'][i]
                publish = page_item['publishs'][i]
                county = self.extract_county_from_bracket(page_item['counties'][i])
                word = page_item['words'][i]
                newspaper = page_item['newspapers'][i]
                download_page = page_item['download_pages'][i]

                article_item = ArticleItem(site=site, keyword=keyword, reprint=reprint, title=title, publish=publish,
                                           county=county, word=word, newspaper=newspaper, download_page=download_page)
                print 'Writting the data into the json file now..........'
                filename = site
                article_item.write_into_json_file(filename)

        elif spider.name == 'WNO':
            articles_in_page_count = len(page_item['site'])
            if articles_in_page_count > 0:
                site = page_item['site'][0]
                keyword = page_item['keyword'][0]
                end_date = page_item['end_date'][0]
                start_date = page_item['start_date'][0]
                filename = "{}_{}_{}_{}".format(site, keyword, start_date, end_date)
                for i in range(articles_in_page_count):
                    title = page_item['titles'][i]
                    title = self.extract_words_from_line_break(title)
                    publish = page_item['publishs'][i]
                    publish = self.extract_date_from_string(publish)
                    description = page_item['descriptions'][i]
                    description = self.extract_words_from_line_break(description)
                    # description = description.decode('unicode_escape')
                    type_ = self.extract_words_from_line_break(page_item['types'][i])
                    words = self.extract_number_from_string(page_item['words'][i])
                    newspaper = self.extract_words_from_line_break(page_item['newspapers'][i])
                    page = self.extract_number_from_string(page_item['pages'][i])
                    download_page = page_item['download_pages'][i]
                    ocr = self.extract_words_from_line_break(page_item['ocrs'][i])
                    search_id = page_item['search_id'][i]
                    article_item = ArticleItem(site=site, keyword=keyword, title=title, publish=publish,
                                               description=description, type_=type_, word=words, newspaper=newspaper,
                                               page=page, download_page=download_page, search_id=search_id,
                                               download_url=download_page, ocr=ocr, start_date=start_date,
                                               end_date=end_date)

                    print 'Writting the data into the json file now..........'
                    article_item.write_into_json_file(filename)
                    article_item.write_into_database(site='WNO')

                dbutils.write_new_search_results(page_item['search_id'][0], filename)


class ArticleItem:

    def __init__(self, title=None, keyword=None, description=None, hint=None, publish=None, newspaper=None,
                 county=None, type_=None, word=None, page=None, tag=None, site=None, reprint=None, download_page=None,
                 download_url=None, ocr=None, start_date=None, end_date=None, search_id=None):
        self.title = title
        self.keyword = keyword
        self.description = description
        self.hint = hint
        self.publish = publish
        self.newspaper = newspaper
        self.county = county
        self.type_ = type_
        self.word = word
        self.page = page
        self.tag = tag
        self.site = site
        self.reprint = reprint
        self.download_page = download_page
        self.download_url = download_url
        self.ocr = ocr
        self.start_date = start_date
        self.end_date = end_date
        self.search_id = search_id

    def write_into_json_file(self, filename):
        with open("Crawler/Records/" + filename + ".json", "a") as f:
            json.dump(self.__dict__, f)
            f.write(',\n')

    def write_into_database(self, site='BNA'):
        publication_date = self.publish
        if site == 'BNA':
            publication_date = datetime.datetime.strptime(self.publish, "%A %d %B %Y")
            publication_date = '{0.year:4d}-{0.month:02d}-{0.day:02d}'.format(publication_date)
        elif site == 'WNO':
            publication_date = self.publish[:4].replace('st', '').replace('nd', '').replace('rd', '').replace('th', '')
            publication_date += self.publish[4:]
            publication_date = datetime.datetime.strptime(publication_date, "%d%B%Y")
            publication_date = '{0.year:4d}-{0.month:02d}-{0.day:02d}'.format(publication_date)
            self.county = ""
        search_result = ArchiveSearchResult(title=self.title.encode('latin-1', 'ignore'),
                                            url=self.download_url.encode('latin-1', 'ignore'),
                                            description=self.description.encode('latin-1', 'ignore'),
                                            publication_title=self.newspaper.encode('latin-1', 'ignore'),
                                            publication_location=self.county.encode('latin-1', 'ignore'),
                                            type=self.type_.encode('latin-1', 'ignore'),
                                            archive_search_id=self.search_id,
                                            publication_date=publication_date,
                                            word_count=self.word,
                                            page=self.page)
        dbconn.insert(search_result)
