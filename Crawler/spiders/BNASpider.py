# -*- coding: utf-8 -*-
from datetime import timedelta, datetime

from scrapy.spiders import Spider
from bs4 import BeautifulSoup
from Crawler.items import PageItem
import scrapy
import os
import csv
from Crawler.utils.databasemodels import ArchiveSearch, ArchiveSearchCount
from Crawler.utils import dbconn
from Crawler.utils import bna_login_utils as login
from Crawler.utils.dbutils import session_scope
from Crawler.utils.ocr import get_ocr_bna
from w3lib.html import remove_tags
from string import join
from openpyxl import load_workbook
from Crawler.utils.advanced_search import AdvancedSearch
import json


class BNASpider(Spider):
    with session_scope() as session:
        name = "BNA"
        allowed_domains = ['britishnewspaperarchive.co.uk']
        search_url = 'https://www.britishnewspaperarchive.co.uk/search/results'
        SITE_NAME = 'britishnewspaperarchive'
        SLASH = '/'
        searchs = []

        filename = 'Crawler/spiders/BNA_search_input.csv'

        fast = False
        generate_json = False
        advanced = False
        url_count = 0
        recovery = False
        start_from_row = 0
        recovery_search_id = 0
        recover_url = None
        counting = False
        split = None
        rec_date_partition = -1

        advanced_search_filepath = 'Crawler/spiders/BNA_advanced_search.xlsx'

        page_count = 0

        def __str__(self):
            return "Spider details: " + json.dumps({
                'name': self.name,
                'allowed domains': self.allowed_domains,
                'search_url': self.search_url,
                'filename': self.filename,
                'mode': 'recovery' if self.recovery else 'fast' if self.fast else 'counting' if self.counting else
                'slow',
                'generate_json': self.generate_json,
                'search': 'advanced' if self.advanced else 'basic',
                'split': self.split
            }, indent=2)

        def __init__(self, mode='slow', generate_json='false', search='basic', split='none', *args, **kwargs):
            super(BNASpider, self).__init__(*args, **kwargs)
            if mode == "recovery":
                self.recovery = True
                with open('recovery', 'r') as recovery_file:
                    lines = recovery_file.read().splitlines()
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
                    self.split = lines[6]
                    self.rec_date_partition = int(lines[7])
            else:
                if mode == "fast":
                    self.fast = True
                elif mode == "count":
                    self.counting = True
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
                if split == 'day' or split == 'week' or split == 'month' or split == 'year':
                    self.split = split
                elif split != 'none':
                    raise Exception('Not supported split. Admited values: day, week, month, year')
            print self
            self.page_count = 0

            if self.advanced:
                print 'Reading advanced search input file\n'
                wb = load_workbook(filename=self.advanced_search_filepath, read_only=True)
                ws = wb['Search']
                count = 0
                first = True
                print 'URLS:'
                for row in list(ws.rows)[self.start_from_row + 1:]:
                    empty = True
                    for j in range(0, 3):
                        if row[j].value is not None:
                            empty = False
                            break
                    if not empty:
                        advanced_search = AdvancedSearch.from_row(row)
                        td = advanced_search.todate
                        fd = advanced_search.fromdate
                        if td is not None and fd is not None:
                            td_date = datetime.strptime(td, '%Y-%m-%d')
                            fd_date = datetime.strptime(fd, '%Y-%m-%d')
                            search_dates = self.split_dates(fd_date, td_date)
                            date_pairs = list(search_dates)
                            date_partition = self.rec_date_partition
                            for date_pair in date_pairs[self.rec_date_partition + 1:]:
                                derived_search = AdvancedSearch.copy_item(advanced_search)
                                dfd = date_pair[0]
                                dtd = date_pair[1]
                                derived_search.fromdate = '%04d-%02d-%02d' % (dfd.year, dfd.month, dfd.day)
                                derived_search.todate = '%04d-%02d-%02d' % (dtd.year, dtd.month, dtd.day)
                                url = self.recover_url if self.recovery and first else derived_search.get_url()
                                first = False
                                if not self.counting:
                                    archive_search = ArchiveSearch(archive=self.SITE_NAME,
                                                                   search_text=derived_search.get_basic_search_string(),
                                                                   archive_date_start=derived_search.fromdate,
                                                                   archive_date_end=derived_search.todate,
                                                                   search_batch_id=self.name,
                                                                   added_date_start=derived_search.fromaddeddate,
                                                                   added_date_end=derived_search.toaddeddate,
                                                                   article_type=derived_search.article_type,
                                                                   exact_phrase=derived_search.exact_phrase,
                                                                   exact_search=derived_search.exact_search,
                                                                   exclude_words=derived_search.exclude_words,
                                                                   front_page=derived_search.front_page,
                                                                   newspaper_title=derived_search.newspaper_title,
                                                                   publication_place=derived_search.place,
                                                                   search_all_words=derived_search.all_words,
                                                                   sort_by=derived_search.sort,
                                                                   tags=derived_search.tags)
                                else:
                                    archive_search = ArchiveSearchCount(archive=self.SITE_NAME,
                                                                        search_text=derived_search.
                                                                        get_basic_search_string(),
                                                                        archive_date_start=derived_search.fromdate,
                                                                        archive_date_end=derived_search.todate,
                                                                        search_batch_id=self.name,
                                                                        added_date_start=derived_search.fromaddeddate,
                                                                        added_date_end=derived_search.toaddeddate,
                                                                        article_type=derived_search.article_type,
                                                                        exact_phrase=derived_search.exact_phrase,
                                                                        exact_search=derived_search.exact_search,
                                                                        exclude_words=derived_search.exclude_words,
                                                                        front_page=derived_search.front_page,
                                                                        newspaper_title=derived_search.newspaper_title,
                                                                        publication_place=derived_search.place,
                                                                        search_all_words=derived_search.all_words,
                                                                        sort_by=derived_search.sort,
                                                                        tags=derived_search.tags)
                                self.searchs.append(dict(url=url,
                                                         search_number=count,
                                                         date_partition=date_partition,
                                                         search_db=archive_search,
                                                         advanced_search=derived_search))
                                date_partition += 1
                                print ' - ' + derived_search.get_url()
                        else:
                            url = self.recover_url if self.recovery and first else advanced_search.get_url()
                            first = False
                            if not self.counting:
                                archive_search = ArchiveSearch(archive=self.SITE_NAME,
                                                               search_text=advanced_search.get_basic_search_string(),
                                                               archive_date_start=fd if fd is not None else '',
                                                               archive_date_end=td if td is not None else '',
                                                               search_batch_id=self.name,
                                                               added_date_start=advanced_search.fromaddeddate,
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
                                                               tags=advanced_search.tags)
                            else:
                                archive_search = ArchiveSearchCount(archive=self.SITE_NAME,
                                                                    search_text=advanced_search.
                                                                    get_basic_search_string(),
                                                                    archive_date_start=fd if fd is not None else '',
                                                                    archive_date_end=td if td is not None else '',
                                                                    search_batch_id=self.name,
                                                                    added_date_start=advanced_search.fromaddeddate,
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
                                                                    tags=advanced_search.tags)
                            self.searchs.append(dict(url=url,
                                                     search_number=count,
                                                     date_partition=0,
                                                     search_db=archive_search,
                                                     advanced_search=advanced_search))
                            print ' - ' + advanced_search.get_url()
                    count += 1
                    self.rec_date_partition = -1
                wb.close()
            else:
                if os.path.exists(self.filename):
                    print 'Reading search input file'
                    with open(self.filename, 'rb') as csv_file:
                        reader = csv.DictReader(csv_file)
                        search_keywords = [row for row in reader]
                    print search_keywords
                else:
                    raise Exception('BNA Spider ERROR: ' + self.filename + ' was not found. Check if it exists.')
                count = 0
                if self.recovery:
                    print "Start from row ", self.start_from_row
                print 'SEARCHES: '
                for i in range(len(search_keywords)):
                    if self.recovery:
                        if i < self.start_from_row:
                            continue
                    fd = search_keywords[i]['start day(xxxx-xx-xx)']
                    td = search_keywords[i]['end day(xxxx-xx-xx)']
                    fd_date = datetime.strptime(fd, '%Y-%m-%d')
                    td_date = datetime.strptime(td, '%Y-%m-%d')
                    search_dates = self.split_dates(fd_date, td_date)
                    date_pairs = list(search_dates)
                    date_partition = self.rec_date_partition
                    for date_pair in date_pairs[date_partition + 1:]:
                        dfd = '%04d-%02d-%02d' % (date_pair[0].year, date_pair[0].month, date_pair[0].day)
                        dtd = '%04d-%02d-%02d' % (date_pair[1].year, date_pair[1].month, date_pair[1].day)
                        url = self.recover_url if self.recovery else (self.search_url + '/' + dfd + '/' + dtd +
                                                                      '?basicsearch=' +
                                                                      search_keywords[i]['keyword'] +
                                                                      '&retrievecountrycounts=false&page=0')
                        if not self.counting:
                            archive_search = ArchiveSearch(archive="britishnewspaperarchive",
                                                           search_text=search_keywords[i]['keyword'],
                                                           archive_date_start=dfd,
                                                           archive_date_end=dtd,
                                                           search_batch_id="BNA")
                        else:
                            archive_search = ArchiveSearchCount(archive="britishnewspaperarchive",
                                                                search_text=search_keywords[i]['keyword'],
                                                                archive_date_start=dfd,
                                                                archive_date_end=dtd,
                                                                search_batch_id="BNA")
                        self.searchs.append(dict(url=url,
                                                 search_number=count,
                                                 date_partition=date_partition,
                                                 search_db=archive_search,
                                                 advanced_search=None))
                        date_partition += 1
                        print ' - ', url
                    count += 1
                    self.rec_date_partition = -1

        def start_requests(self):
            if self.counting:
                for search in self.searchs:
                    yield scrapy.Request(search["url"], meta={"search": search},
                                         callback=self.count_callback)
            else:
                if not self.recovery:
                    initialize_search_file()
                if not self.fast:
                    print 'BNA Spider: Logging in'
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
                    for search in self.searchs:
                        yield scrapy.Request(search["url"], meta={"search": search})

        def after_login(self, response):
            cookie = None
            for cookie_item in response.headers.getlist('Set-Cookie'):
                cookie = cookie_item.split(';')[0].split('session_0=')[1]
                if cookie != '':
                    break
            session_cookies = {'session_0': cookie}
            if cookie == '':
                print 'BNA Spider: Problem trying to logging in (Cookie not found)'
            else:
                print 'BNA Spider: Successful login. \n'
                for search in self.searchs:
                    yield scrapy.Request(search["url"], meta={"search": search},
                                         cookies=session_cookies)

        def count_callback(self, response):
            search = response.meta['search']
            if self.advanced:
                identifier = search["advanced_search"].get_basic_search_string()
            else:
                identifier = search["search_db"].search_text

            article_amounts = response.selector.css('#dateFacet div#date a.list-group-item')
            article_count = 0
            for article_amount in article_amounts:
                article_count += int(article_amount.css('span::text').extract_first().replace(',', ''))
            archive_search = search["search_db"]
            archive_search.results_count = article_count
            yield dict(identifier=identifier, search_count=archive_search)

        def parse(self, response):
            self.page_count += 1
            session_cookies = {}
            if not self.fast:
                cookie_str = response.request.headers.getlist('Cookie')[0].split(';')[0].split('session_0=')[1]
                session_cookies = {'session_0': cookie_str}
            search = response.meta['search']
            advanced_search = search["advanced_search"]
            archive_search = search["search_db"]
            page = PageItem()
            if self.advanced:
                print 'Crawling page %d - "%s [%s - %s]"' % (self.page_count,
                                                             advanced_search.get_basic_search_string(),
                                                             advanced_search.fromdate,
                                                             advanced_search.todate)
                page['keyword'] = advanced_search.get_search_input()
                start_date = advanced_search.fromdate
                end_date = advanced_search.todate
                page['start_date'] = start_date if start_date is not None else ''
                page['end_date'] = end_date if end_date is not None else ''
            else:
                print 'Crawling page %d - "%s [%s - %s]"' % (self.page_count,
                                                             archive_search.search_text,
                                                             archive_search.archive_date_start,
                                                             archive_search.archive_date_end)
                page['keyword'] = archive_search.search_text
                page['start_date'] = archive_search.archive_date_start
                page['end_date'] = archive_search.archive_date_end
            page['site'] = self.SITE_NAME
            search_id = archive_search.id
            if search_id == 0 or search_id is None:
                avoid_appending = False
                if self.page_count == 1 and self.recovery:
                    search_id = self.recovery_search_id
                    avoid_appending = True
                else:
                    dbconn.insert_search(self.session, archive_search)
                    print "Search inserted into the database"
                    search_id = archive_search.id
                if not avoid_appending:
                    self.write_search(archive_search, advanced_search)

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
                self.create_recovery_file(search_id, next_page_full_url,
                                          search["search_number"], search["date_partition"])
                yield scrapy.Request(next_page_full_url, meta={"search": search}, headers=login.headers)
            else:
                self.page_count = 0

        def parse_details(self, url, cookies):
            link = url.split('bl')[1]
            ocr_text = ''
            if not self.fast:
                ocr_text = get_ocr_bna(url, cookies)
            download_url = 'https://www.britishnewspaperarchive.co.uk/viewer/download/bl' + link
            return download_url, ocr_text

        def write_search(self, search, search_identifier=None):
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
                    kw = search.search_text
                    start_date = search.archive_date_start
                    end_date = search.archive_date_end
                    writer.writerow([s_id, "{}_{}_{}_{}".format(site, kw, start_date, end_date)])

        def write_searches(self):
            with open('search_ids.csv', 'wb') as search_file:
                writer = csv.writer(search_file)
                writer.writerow(['id', 'filename'])
                for search in self.searchs:
                    s_db = search["search_db"]
                    s_id = s_db.id
                    site = s_db.archive
                    if self.advanced:
                        advanced_search = search["advanced_search"]
                        kw = advanced_search.get_search_input()
                        start_date = advanced_search.fromdate
                        end_date = advanced_search.todate
                        writer.writerow([s_id, "{}_{}_{}_{}".format(site, kw, start_date, end_date)])
                    else:
                        kw = s_db.search_text
                        start_date = s_db.archive_date_start
                        end_date = s_db.archive_date_end
                        writer.writerow([s_id, "{}_{}_{}_{}".format(site, kw, start_date, end_date)])

        def create_recovery_file(self, last_search, next_page, row, last_date_partition):
            with open('recovery', 'w+') as page_err:
                values = [str(row + self.start_from_row),
                          str(last_search),
                          str(self.fast),
                          str(self.generate_json),
                          str(self.advanced),
                          next_page,
                          str(self.split),
                          str(last_date_partition)]
                separator = '\n'
                page_err.write(separator.join(values))

        def split_dates(self, from_date, to_date):
            delta = to_date - from_date
            days = delta.days
            if self.split is None:
                yield (from_date, to_date)
            else:
                if self.split == 'day':
                    threshold = 1
                elif self.split == 'week':
                    threshold = 6
                elif self.split == 'month':
                    threshold = 29
                else:
                    threshold = 364
                if threshold >= days:
                    yield (from_date, to_date)
                else:
                    aux_date = from_date
                    for i in range(0, days + 1, threshold + 1):
                        aux_end_date = aux_date + timedelta(days=threshold)
                        if aux_end_date > to_date:
                            yield (aux_date, to_date)
                        else:
                            aux_start_date = aux_date
                            aux_date = aux_end_date + timedelta(days=1)
                            yield (aux_start_date, aux_end_date)


def initialize_search_file():
    with open('search_ids.csv', 'w') as search_file:
        writer = csv.writer(search_file)
        writer.writerow(['id', 'filename'])
