# -*- coding: utf-8 -*-
import re
import json
from Crawler.utils.databasemodels import ArchiveSearchResult, CandidateDocument
from Crawler.utils import dbconn
import datetime

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from Crawler.utils.dbutils import session_scope


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
            articles_in_page_count = len(page_item['titles'])
            if articles_in_page_count > 0:
                site = page_item['site']
                keyword = page_item['keyword']
                start_date = page_item['start_date']
                end_date = page_item['end_date']
                generate_json = page_item['generate_json']
                search_id = page_item['search_id']
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
                    download_page = page_item['download_pages'][i]
                    download_url = page_item['download_urls'][i]
                    ocr = page_item['ocrs'][i]

                    article_item = ArticleItem(site=site, title=title, description=description,
                                               hint=hint, publish=publish, newspaper=newspaper, county=county,
                                               type_=type_, word=word, page=page, tag=tag, download_url=download_url,
                                               download_page=download_page, ocr=ocr, start_date=start_date,
                                               end_date=end_date, search_id=search_id)

                    if generate_json:
                        print 'Writing data into the json file'
                        article_item.write_into_json_file(filename)
                    else:
                        print 'Writing data only into database'
                        filename = None
                    article_item.write_into_database(filename=filename)

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

                article_item = ArticleItem(site=site, reprint=reprint, title=title, publish=publish,
                                           county=county, word=word, newspaper=newspaper, download_page=download_page)
                print 'Writting the data into the json file now..........'
                filename = site
                article_item.write_into_json_file(filename)

        elif spider.name == 'WNO':
            articles_in_page_count = len(page_item['site'])
            if articles_in_page_count > 0:
                site = page_item['site']
                keyword = page_item['keyword']
                start_date = page_item['start_date']
                end_date = page_item['end_date']
                search_id = page_item['search_id']
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
                    article_item = ArticleItem(site=site, title=title, publish=publish,
                                               description=description, type_=type_, word=words, newspaper=newspaper,
                                               page=page, download_page=download_page, search_id=search_id,
                                               download_url=download_page, ocr=ocr, start_date=start_date,
                                               end_date=end_date)

                    print 'Writting the data into the json file now..........'
                    article_item.write_into_json_file(filename)
                    article_item.write_into_database(site='WNO')


class ArticleItem:

    def __init__(self, title=None, description=None, hint=None, publish=None, newspaper=None,
                 county=None, type_=None, word=None, page=None, tag=None, site=None, reprint=None, download_page=None,
                 download_url=None, ocr=None, start_date=None, end_date=None, search_id=None):
        self.title = title
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

    def write_into_database(self, site='BNA', filename=None):
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
                                            word_count=self.word)
        with session_scope() as session:
            dbconn.insert(session, search_result)
            unique_result = session.query(CandidateDocument.id)\
                .filter(CandidateDocument.url == search_result.url).first()
            if unique_result is None:
                ocr = ""
                page = 0
                try:
                    full_json_path = "Crawler/Records/" + filename + ".json"
                    with open(full_json_path, 'rb') as json_file:
                        info = json_file.read()
                        info = info.strip()
                        info = "[" + info[:-1] + "]"
                        jarray = json.loads(info)
                        jarticle = next((row for row in jarray if row['download_url'] == search_result.url), None)
                        if jarticle is None:
                            jarticle = next((row for row in jarray if row['download_page'] == search_result.url),
                                            None)
                        if jarticle is not None:
                            ocr = jarticle["ocr"]
                            page = int(jarticle["page"])
                except:
                    if 'britishnewspaper' in search_result.url:
                        page = int(search_result.url.split('/')[-1])
                candidate_document = CandidateDocument(title=search_result.title,
                                                       url=search_result.url,
                                                       description=search_result.description,
                                                       publication_title=search_result.publication_title,
                                                       publication_location=search_result.publication_location,
                                                       type=search_result.type,
                                                       publication_date=search_result.publication_date,
                                                       status="", g_status="", status_writer="gary",
                                                       word_count=search_result.word_count,
                                                       page=page,
                                                       ocr=ocr.encode('latin-1', 'ignore'))
                dbconn.insert(session, candidate_document)
