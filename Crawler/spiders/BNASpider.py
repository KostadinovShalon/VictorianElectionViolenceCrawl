# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from bs4 import BeautifulSoup

from Crawler.items import PageItem
import scrapy
import os
import csv
from Crawler.utils.databasemodels import ArchiveSearch
from Crawler.utils import dbconn
from Crawler.utils import bna_login_utils as login
from Crawler.utils.dbutils import session_scope
from Crawler.utils.ocr import get_ocr_bna
from w3lib.html import remove_tags
from string import join
from openpyxl import load_workbook
from Crawler.utils.advanced_search import AdvancedSearch


class BNASpider(Spider):

    with session_scope() as session:
        name = "BNA"
        allowed_domains = ['britishnewspaperarchive.co.uk']

        search_url = 'https://www.britishnewspaperarchive.co.uk/search/results'
        SITE_NAME = 'britishnewspaperarchive'
        search_key_words = []
        advanced_searchs = []
        SLASH = '/'

        filename = 'Crawler/spiders/BNA_search_input.csv'

        parse_urls = []
        search_db = []

        def __init__(self, mode='slow', generate_json='false', search='basic', *args, **kwargs):
            super(BNASpider, self).__init__(*args, **kwargs)
            self.fast = False
            self.generate_json = False
            self.advanced = False
            self.url_count = 0
            self.recovery = False
            self.start_from_row = 0
            self.recovery_search_id = 0
            self.recover_url = None
            if mode == "recovery":
                self.recovery = True
                with open('recovery', 'r') as recovery_file:
                    lines = recovery_file.read().splitlines()
                    print lines
                    self.start_from_row = int(lines[0])
                    self.recovery_search_id = int(lines[1])
                    self.fast = lines[2] == "True"
                    if self.fast:
                        self.mode = "fast"
                    else:
                        self.mode = "slow"
                    self.generate_json = lines[3] == "True"
                    self.advanced = lines[4] == "True"
                    print self.advanced
                    self.recover_url = lines[5]
            else:
                if mode == "fast":
                    self.fast = True
                elif mode != "slow":
                    raise Exception('Not supported mode')
                if generate_json == 'true':
                    self.generate_json = True
                elif generate_json != 'false':
                    raise Exception('Not supported generate_json value')
                if search == 'advanced':
                    self.advanced = True
                elif search != 'basic':
                    raise Exception('Search mode can only be either advanced or basic')

            if self.advanced:
                wb = load_workbook(filename='Crawler/spiders/BNA_advanced_search.xlsx', read_only=True)
                ws = wb['Search']
                count = 0
                first = True
                for row in list(ws.rows)[self.start_from_row + 1:]:
                    empty = True
                    for j in range(0, 3):
                        if row[j].value is not None:
                            empty = False
                            break
                    if not empty:
                        advanced_search = AdvancedSearch(row)
                        td = advanced_search.todate
                        fd = advanced_search.fromdate
                        self.advanced_searchs.append(advanced_search)
                        if self.recovery and first:
                            self.parse_urls.append((self.recover_url, count))
                            first = False
                        else:
                            self.parse_urls.append((advanced_search.get_url(), count))
                        count = count + 1
                        self.search_db.append(
                            ArchiveSearch(archive="britishnewspaperarchive",
                                          search_text=advanced_search.get_basic_search_string(),
                                          archive_date_start=fd if fd is not None else '',
                                          archive_date_end=td if td is not None else '',
                                          search_batch_id="BNA", added_date_start=advanced_search.fromaddeddate,
                                          added_date_end=advanced_search.toaddeddate,
                                          article_type=advanced_search.article_type,
                                          exact_phrase=advanced_search.exact_phrase,
                                          exact_search=advanced_search.exact_search,
                                          exclude_words=advanced_search.exclude_words,
                                          front_page=advanced_search.front_page,
                                          newspaper_title=advanced_search.newspaper_title,
                                          publication_place=advanced_search.place,
                                          search_all_words=advanced_search.all_words,
                                          sort_by=advanced_search.sort,
                                          tags=advanced_search.tags))
                        print advanced_search.get_url()
                wb.close()
            else:
                if os.path.exists(self.filename):
                    print 'BNA Spider: Reading BNA input file\n'
                    with open(self.filename, 'rb') as csv_file:
                        reader = csv.DictReader(csv_file)
                        self.search_key_words = [row for row in reader]
                    print self.search_key_words
                else:
                    print 'BNA Spider: ' + self.filename + ' was not found. Check if it exists.'
                count = 0
                print "start from row", self.start_from_row
                for i in range(len(self.search_key_words)):
                    if self.recovery:
                        if i < self.start_from_row:
                            continue
                    self.search_db.append(
                        ArchiveSearch(archive="britishnewspaperarchive",
                                      search_text=self.search_key_words[i]['keyword'],
                                      archive_date_start=self.search_key_words[i]['start day(xxxx-xx-xx)'],
                                      archive_date_end=self.search_key_words[i]['end day(xxxx-xx-xx)'],
                                      search_batch_id="BNA"))
                    if self.recovery and i == self.start_from_row:
                        self.parse_urls.append((self.recover_url, count))
                    else:
                        self.parse_urls.append((self.search_url + '/' + self.search_key_words[i]['start day(xxxx-xx-xx)'] +
                                                '/' + self.search_key_words[i]['end day(xxxx-xx-xx)'] +
                                                '?basicsearch=' + self.search_key_words[i]['keyword'] +
                                                '&retrievecountrycounts=false&page=0', count))
                    count = count + 1
                self.search_key_words = self.search_key_words[self.start_from_row:]
                print self.parse_urls

        def start_requests(self):
            if not self.recovery:
                self.initialize_search_file()
            if not self.fast:
                print 'BNA Spider: Logging in\n'
                yield scrapy.FormRequest(url=login.login_url,
                                         headers=login.headers,
                                         meta={
                                             'dont_redirect': True,
                                             'handle_httpstatus_list': [302]
                                         },
                                         formdata={
                                             'Username': login.username,
                                             'Password': login.password,
                                             'RememberMe': login.remember_me,
                                             'NextPage': login.next_page
                                         },
                                         callback=self.after_login,
                                         dont_filter=False)
            else:
                # for search in self.search_db:
                #     dbconn.insert_search(self.session, search)
                # self.write_searchs()
                for url in self.parse_urls:
                    yield scrapy.Request(url[0], meta={"keyword_count": url[1]})

        def after_login(self, response):
            cookie = ''
            for scookie in response.headers.getlist('Set-Cookie'):
                cookie = scookie.split(';')[0].split('session_0=')[1]
                if cookie != '':
                    break

            session_cookies = {'session_0': cookie}
            if cookie == '':
                print 'BNA Spider: Problem trying to logging in (Cookie not found)\n'
            else:
                print 'BNA Spider: Successful login. \n'
                # for search in self.search_db:
                #     dbconn.insert_search(self.session, search)
                # self.write_searchs()
                for url in self.parse_urls:
                    yield scrapy.Request(url[0], meta={"keyword_count": url[1]}, cookies=session_cookies)

        def parse(self, response):
            session_cookies = {}
            if not self.fast:
                cookie_str = response.request.headers.getlist('Cookie')[0].split(';')[0].split('session_0=')[1]
                session_cookies = {'session_0': cookie_str}
            keyword_count = response.meta['keyword_count']
            page = PageItem()
            if self.advanced:
                print 'BNA Spider: Crawling ', self.advanced_searchs[keyword_count].get_basic_search_string()
                page['keyword'] = self.advanced_searchs[keyword_count].get_search_input()
                start_date = self.advanced_searchs[keyword_count].fromdate
                end_date = self.advanced_searchs[keyword_count].todate
                page['start_date'] = start_date if start_date is not None else ''
                page['end_date'] = end_date if end_date is not None else ''
            else:
                print 'BNA Spider: Crawling ', self.search_key_words[keyword_count]['keyword']
                page['keyword'] = self.search_key_words[keyword_count]['keyword']
                page['start_date'] = self.search_key_words[keyword_count]['start day(xxxx-xx-xx)']
                page['end_date'] = self.search_key_words[keyword_count]['end day(xxxx-xx-xx)']

            page['site'] = self.SITE_NAME
            search_id = self.search_db[keyword_count].id
            if search_id == 0 or search_id is None:
                avoid_appending = False
                if keyword_count == 0 and self.recovery:
                    search_id = self.recovery_search_id
                    avoid_appending = True
                else:
                    dbconn.insert_search(self.session, self.search_db[keyword_count])
                    search_id = self.search_db[keyword_count].id
                if not avoid_appending:
                    if self.advanced:
                        self.write_search(self.search_db[keyword_count],
                                          self.advanced_searchs[keyword_count])
                    else:
                        self.write_search(self.search_db[keyword_count],
                                          self.search_key_words[keyword_count])

            page['generate_json'] = self.generate_json
            page['search_id'] = search_id
            page['titles'] = []
            page['hints'] = []
            page['descriptions'] = []
            page['publishs'] = []
            page['counties'] = []
            page['types'] = []
            page['words'] = []
            page['pages'] = []
            page['tags'] = []
            page['newspapers'] = []
            page['download_pages'] = []
            page['download_urls'] = []
            page['ocrs'] = []

            all_articles = response.selector.css('article.bna-card')
            for article in all_articles:
                # To get the title text
                this_title = article.css('h4.bna-card__title')

                article_detail_url = response.urljoin(this_title.css('a::attr(href)').extract_first())
                page['download_pages'].append(article_detail_url)
                download_url, ocr = self.parse_details(article_detail_url, cookies=session_cookies)
                page['download_urls'].append(download_url)
                page['ocrs'].append(ocr)
                page['titles'].append(this_title.css('a::text').extract_first().strip())
                page['hints'].append(remove_tags(this_title.css('a::attr(title)').extract_first().strip()))
                page['descriptions'].append(join(article.css('p.bna-card__body__description::text').extract()).strip())

                meta = BeautifulSoup(article.css('div.bna-card__meta').extract_first(), 'html.parser')
                page['publishs'].append(meta.small.span.get_text().split("Published:")[1].strip())
                for item in meta.small.span.find_next_siblings("span"):
                    item_str = item.get_text().encode('utf-8')
                    if 'Newspaper' in item_str:
                        page['newspapers'].append(item_str.split('Newspaper:\n')[1])
                    elif 'County' in item_str:
                        # print item_str.split(('County:\n')[1])
                        page['counties'].append(item_str.split('\nCounty: \r\n')[1])
                    elif 'Type' in item_str:
                        page['types'].append(item_str.split('\nType:')[1])
                    elif 'Word' in item_str:
                        # print item_str.split('\nWords: \r\n')
                        page['words'].append(item_str.split('\nWords: \r\n')[1])
                    elif 'Page' in item_str:
                        # print item_str.split('\nPage:')
                        page['pages'].append(item_str.split('\nPage:')[1])
                    elif 'Tag' in item_str:
                        # print item_str.split('\nTags:\n')
                        page['tags'].append(item_str.split('\nTags:\n')[1])
                    else:
                        print 'Error'
            yield page

            next_page = response.selector.css('a[title="Forward one page"]::attr(href)').extract_first()
            if next_page is not None:
                next_page_full_url = response.urljoin(next_page)
                self.create_recovery_file(search_id, next_page_full_url, keyword_count)
                yield scrapy.Request(next_page_full_url, meta={"keyword_count": keyword_count}, headers=login.headers)

        def parse_details(self, url, cookies):
            link = url.split('bl')[1]
            ocr_text = ''
            if not self.fast:
                ocr_text = get_ocr_bna(url, cookies)
            download_url = 'https://www.britishnewspaperarchive.co.uk/viewer/download/bl' + link
            return download_url, ocr_text

        def initialize_search_file(self):
            with open('search_ids.csv', 'w') as search_file:
                writer = csv.writer(search_file)
                writer.writerow(['id', 'filename'])

        def write_search(self, search, search_identifier):
            with open('search_ids.csv', 'a+') as search_file:
                writer = csv.writer(search_file)
                s_id = search.id
                if s_id is None and self.recovery:
                    s_id = self.recovery_search_id
                site = search.archive
                if self.advanced:
                    advanced_search = search_identifier
                    kw = advanced_search.get_search_input()
                    start_date = advanced_search.fromdate
                    end_date = advanced_search.todate
                    writer.writerow([s_id, "{}_{}_{}_{}".format(site, kw, start_date, end_date)])
                else:
                    kw = search_identifier['keyword']
                    start_date = search_identifier['start day(xxxx-xx-xx)']
                    end_date = search_identifier['end day(xxxx-xx-xx)']
                    writer.writerow([s_id, "{}_{}_{}_{}".format(site, kw, start_date, end_date)])

        def write_searchs(self):
            with open('search_ids.csv', 'wb') as search_file:
                writer = csv.writer(search_file)
                writer.writerow(['id', 'filename'])
                for i in range(len(self.search_db)):
                    s_db = self.search_db[i]
                    s_id = s_db.id
                    site = s_db.archive
                    if self.advanced:
                        advanced_search = self.advanced_searchs[i]
                        kw = advanced_search.get_search_input()
                        start_date = advanced_search.fromdate
                        end_date = advanced_search.todate
                        writer.writerow([s_id, "{}_{}_{}_{}".format(site, kw, start_date, end_date)])
                    else:
                        kw = self.search_key_words[i]['keyword']
                        start_date = self.search_key_words[i]['start day(xxxx-xx-xx)']
                        end_date = self.search_key_words[i]['end day(xxxx-xx-xx)']
                        writer.writerow([s_id, "{}_{}_{}_{}".format(site, kw, start_date, end_date)])

        def create_recovery_file(self, last_search, next_page, row):
            with open('recovery', 'w+') as page_err:
                values = [str(row + self.start_from_row),
                          str(last_search),
                          str(self.fast),
                          str(self.generate_json),
                          str(self.advanced),
                          next_page]
                separator = '\n'
                page_err.write(separator.join(values))
