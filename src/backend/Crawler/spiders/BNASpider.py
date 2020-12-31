# -*- coding: utf-8 -*-
import json
from datetime import timedelta, datetime

import scrapy
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from scrapy.spiders import Spider
from w3lib.html import remove_tags

from Crawler.items import PageItem
from repositories import repo_handler, configuration
from db.databasemodels import ArchiveSearch, ArchiveSearchCount
from Crawler.utils import headers
from Crawler.utils.ocr import get_ocr_bna
from Crawler.utils.search_terms import RecoveryAdvancedSearchTerms, AdvancedSearchTerms, RecoverySearchTerms


class GeneralBNASpider(Spider):
    name = "BNA"
    allowed_domains = ['britishnewspaperarchive.co.uk']
    search_url = 'https://www.britishnewspaperarchive.co.uk/search/results'
    site_name = 'britishnewspaperarchive'

    page_count = 0

    # todo: ask to user if want to recover fast or slow
    # TODO: change recovery implementation to multi-entries

    def __init__(self, search_terms, advanced=False, split=None, recovery=False,
                 *args, **kwargs):
        super(GeneralBNASpider, self).__init__(*args, **kwargs)
        self.searches = []
        self.n_search = 0
        self.headers = headers

        self.url_count = 0
        self.start_from_row = 0
        self.recover_url = None
        self.rec_date_partition = -1
        self.recovery = recovery

        self.search_terms = search_terms
        self.advanced = advanced
        self.page_count = 0
        self.split = None
        self.total_articles = 0
        self.derived_search_terms = []

        try:
            self.split = int(split)
        except ValueError:
            if split == 'day' or split == 'week' or split == 'month' or split == 'year':
                self.split = split
            elif split != 'none':
                raise Exception('Not supported split. Admited values: day, week, month, year')
        except TypeError:
            if split is not None:
                raise Exception('Not supported split. Admited values: day, week, month, year')

        if recovery:
            assert isinstance(search_terms, RecoveryAdvancedSearchTerms) or \
                   isinstance(search_terms, RecoverySearchTerms)
            self._read_recovery_file()
        print(search_terms)
        if self.advanced:
            print("In generate advanced")
            self._generate_advanced_searches()
        else:
            print("Number of searches:", len(search_terms))
            self._generate_basic_searches()

    def _generate_advanced_searches(self):
        first = True
        search_terms = self.search_terms
        if not isinstance(search_terms, list):
            search_terms = [search_terms]
        for count, advanced_search in enumerate(search_terms):
            if self.recovery:
                if count < self.start_from_row:
                    continue
            if advanced_search.all_words is not None or advanced_search.some_words is not None or \
                    advanced_search.exact_phrase is not None:
                td = advanced_search.end_date
                fd = advanced_search.start_date
                if td is not None and fd is not None:
                    td_date = datetime.strptime(td, '%Y-%m-%d')
                    fd_date = datetime.strptime(fd, '%Y-%m-%d')
                    search_dates = self.split_dates(fd_date, td_date)
                    date_pairs = list(search_dates)
                    date_partition = self.rec_date_partition
                    for date_pair in date_pairs[self.rec_date_partition + 1:]:
                        derived_search = advanced_search.copy()
                        dfd = date_pair[0]
                        dtd = date_pair[1]
                        derived_search.start_date = '%04d-%02d-%02d' % (dfd.year, dfd.month, dfd.day)
                        derived_search.end_date = '%04d-%02d-%02d' % (dtd.year, dtd.month, dtd.day)
                        url = self.recover_url if self.recovery and first else derived_search.get_url()
                        first = False
                        archive_search = self.get_archive_search(derived_search)
                        self.searches.append(dict(url=url,
                                                  search_number=count,
                                                  date_partition=date_partition,
                                                  search_db=archive_search,
                                                  advanced_search=derived_search))
                        date_partition += 1
                        self.derived_search_terms.append(derived_search.to_dict())
                else:
                    url = self.recover_url if self.recovery and first else advanced_search.get_url()
                    first = False
                    archive_search = self.get_archive_search(advanced_search)
                    self.searches.append(dict(url=url,
                                              search_number=count,
                                              date_partition=0,
                                              search_db=archive_search,
                                              advanced_search=advanced_search))
            self.rec_date_partition = -1

    def get_archive_search(self, search):
        if isinstance(search, AdvancedSearchTerms):
            return ArchiveSearch(archive=self.site_name,
                                 search_text=search.get_basic_search_string(),
                                 archive_date_start=search.start_date if search.start_date is not None else '',
                                 archive_date_end=search.end_date if search.end_date is not None else '',
                                 search_batch_id=self.name,
                                 added_date_start=search.added_start_date,
                                 added_date_end=search.added_end_date,
                                 article_type=search.article_type,
                                 exact_phrase=search.exact_phrase,
                                 exact_search=search.exact_search,
                                 exclude_words=search.exclude_words,
                                 front_page=search.front_page,
                                 newspaper_title=search.newspaper_title,
                                 publication_place=search.publication_place,
                                 search_all_words=search.all_words,
                                 sort_by=search.sort_by,
                                 tags=search.tags)
        else:
            return ArchiveSearch(archive=self.site_name,
                                 search_text=search.search_text,
                                 archive_date_start=search.start_date,
                                 archive_date_end=search.end_date,
                                 search_batch_id=self.name)

    def _generate_basic_searches(self):
        first = True
        search_terms = self.search_terms
        if not isinstance(search_terms, list):
            search_terms = [search_terms]
        for count, search_term in enumerate(search_terms):
            if self.recovery:
                if count < self.start_from_row:
                    continue
            fd = search_term.start_date
            td = search_term.end_date
            fd = datetime.strptime(fd, '%Y-%m-%d')
            td = datetime.strptime(td, '%Y-%m-%d')
            search_dates = self.split_dates(fd, td)
            date_pairs = list(search_dates)
            date_partition = self.rec_date_partition

            for date_pair in date_pairs[date_partition + 1:]:
                date_partition += 1
                derived_search = search_term.copy()
                derived_search.start_date = '%04d-%02d-%02d' % (date_pair[0].year, date_pair[0].month, date_pair[0].day)
                derived_search.end_date = '%04d-%02d-%02d' % (date_pair[1].year, date_pair[1].month, date_pair[1].day)
                url = self.recover_url if self.recovery and first else \
                    f"{self.search_url}/{derived_search.start_date}/{derived_search.end_date}" \
                    f"?basicsearch={search_term.search_text}&retrievecountrycounts=false&page=0 "
                first = False
                archive_search = self.get_archive_search(derived_search)
                self.searches.append(dict(url=url,
                                          search_number=count,
                                          date_partition=date_partition,
                                          search_db=archive_search,
                                          advanced_search=None))
                self.derived_search_terms.append(derived_search.to_dict())
            self.rec_date_partition = -1

    def _read_recovery_file(self):
        try:
            with open(f'recovery.{self.search_terms.id}', 'r') as recovery_file:
                lines = recovery_file.read().splitlines()
                self.start_from_row = int(lines[0])
                self.advanced = lines[3] == isinstance(self.search_terms, AdvancedSearchTerms)
                self.recover_url = lines[4]
                self.split = lines[5]
                self.rec_date_partition = int(lines[6])
        except FileNotFoundError:
            raise Exception(f"Recovery file for search id: {self.search_terms.id} not found")

    def __str__(self):
        return "Spider details: " + json.dumps({
            'name': self.name,
            'allowed domains': self.allowed_domains,
            'search_url': self.search_url,
            'mode': 'slow',
            'search': 'advanced' if self.advanced else 'basic',
            'split': self.split
        }, indent=2)

    def start_requests(self):
        yield scrapy.Request(self.searches[0]["url"], meta={"search": self.searches[0]})

    def count_articles(self, response):
        search = response.meta['search']
        if self.advanced:
            identifier = search["advanced_search"].get_basic_search_string()
        else:
            identifier = search["search_db"].search_text

        article_amounts = response.selector.css('#dateFacet div#date a.list-group-item')
        self.total_articles = 0
        if article_amounts is not None and len(article_amounts) > 0:
            for article_amount in article_amounts:
                self.total_articles += int(article_amount.css('span::text').extract_first().replace(',', ''))
        else:
            count_string = response.selector.css('#dateFacet div#date div span:last-child::text').extract_first()
            if count_string is None:
                self.total_articles = 0
            else:
                self.total_articles = int(count_string[1:][:-1])
        archive_search = search["search_db"]
        archive_search.results_count = self.total_articles
        return dict(identifier=identifier, search_count=archive_search)

    def parse(self, response, **kwargs):
        print("Page count:", self.page_count)
        self.page_count += 1

        if self.page_count == 1:
            self.count_articles(response)

        session_cookies = self.get_session_cookies(response)
        search = response.meta['search']
        advanced_search = search["advanced_search"]
        archive_search = search["search_db"]

        search_id = archive_search.id
        if search_id == 0 or search_id is None:
            search_id = repo_handler.insert_search(archive_search)
            print("Search inserted into the database", "Search id: ", search_id)
        search["search_db"].id = search_id

        all_articles = response.selector.css('article.bna-card')
        for article in all_articles:
            # To get the title text
            page = PageItem()
            page["search_index"] = self.n_search
            page['site'] = self.site_name
            page['search_id'] = search_id
            page['total_articles'] = self.total_articles
            if self.advanced:
                page['keyword'] = advanced_search.get_search_input()
                start_date = advanced_search.start_date
                end_date = advanced_search.end_date
                page['start_date'] = start_date if start_date is not None else ''
                page['end_date'] = end_date if end_date is not None else ''
            else:
                page['keyword'] = archive_search.search_text
                page['start_date'] = archive_search.archive_date_start
                page['end_date'] = archive_search.archive_date_end
            this_title = article.css('h4.bna-card__title')

            article_detail_url = response.urljoin(this_title.css('a::attr(href)').extract_first())
            page['download_page'] = article_detail_url
            download_url, ocr = self.parse_details(article_detail_url, cookies=session_cookies)
            page['download_url'] = download_url
            page['ocr'] = ocr
            page['title'] = this_title.css('a::text').extract_first().strip()
            page['hint'] = remove_tags(this_title.css('a::attr(title)').extract_first().strip())
            page['description'] = ".".join(article.css('p.bna-card__body__description::text').extract()).strip()

            meta = BeautifulSoup(article.css('div.bna-card__meta').extract_first(), 'html.parser')
            page['publish'] = meta.small.span.get_text().split("Published:")[1].strip()
            for item in meta.small.span.find_next_siblings("span"):
                item_str = item.get_text()
                if 'Newspaper' in item_str:
                    page['newspaper'] = item_str.split('Newspaper:\n')[1]
                elif 'County' in item_str:
                    # print item_str.split(('County:\n')[1])
                    page['county'] = item_str.split('\nCounty: \r\n')[1]
                elif 'Type' in item_str:
                    page['type'] = item_str.split('\nType:')[1]
                elif 'Word' in item_str:
                    # print item_str.split('\nWords: \r\n')
                    page['word'] = item_str.split('\nWords: \r\n')[1]
                elif 'Page' in item_str:
                    # print item_str.split('\nPage:')
                    page['page'] = item_str.split('\nPage:')[1]
                elif 'Tag' in item_str:
                    # print item_str.split('\nTags:\n')
                    page['tag'] = item_str.split('\nTags:\n')[1]
                else:
                    print('Error')
            yield page

        next_page = response.selector.css('a[title="Forward one page"]::attr(href)').extract_first()
        search["search_db"] = archive_search
        if next_page is not None:
            next_page_full_url = response.urljoin(next_page)
            print("Next page full url", next_page_full_url)
            self.create_recovery_file(search_id, next_page_full_url,
                                      search["search_number"], search["date_partition"])
            print("Yielding new request")
            yield scrapy.Request(next_page_full_url, meta={"search": search}, headers=self.headers)
        else:
            self.page_count = 0
            self.n_search += 1
            if self.n_search < len(self.searches):
                yield scrapy.Request(self.searches[self.n_search]["url"],
                                     meta={"search": self.searches[self.n_search]},
                                     headers=self.headers)

    def get_session_cookies(self, response):
        return {}

    def parse_details(self, url, cookies):
        link = url.split('bl')[1]
        download_url = 'https://www.britishnewspaperarchive.co.uk/viewer/download/bl' + link
        return download_url, ''

    def create_recovery_file(self, last_search, next_page, row, last_date_partition):
        with open('recovery', 'w+') as page_err:
            values = [str(row + self.start_from_row),
                      str(last_search),
                      "False",
                      str(self.advanced),
                      next_page,
                      str(self.split),
                      str(last_date_partition)]
            separator = '\n'
            page_err.write(separator.join(values))

    def split_dates(self, from_date, to_date):
        if self.split is None:
            yield from_date, to_date
        else:
            if isinstance(self.split, int):
                if self.split > 0:
                    time_delta = relativedelta(days=self.split)
                else:
                    yield from_date, to_date
                    return
            elif self.split == 'day':
                time_delta = relativedelta(days=1)
            elif self.split == 'week':
                time_delta = relativedelta(weeks=1)
            elif self.split == 'month':
                time_delta = relativedelta(months=1)
            else:
                time_delta = relativedelta(years=1)
            if from_date + time_delta > to_date:
                yield from_date, to_date
            else:
                aux_date = from_date
                while aux_date < to_date:
                    aux_end_date = (aux_date + time_delta) - timedelta(days=1)
                    if aux_end_date >= to_date:
                        yield aux_date, to_date
                    else:
                        aux_start_date = aux_date
                        yield aux_start_date, aux_end_date
                    aux_date = aux_end_date + timedelta(days=1)


class BNASpiderWithLogin(GeneralBNASpider):
    name = "BNAWithLogin"

    def __init__(self, search_terms, advanced=False, split=None, recovery=False,
                 *args, **kwargs):
        super().__init__(search_terms, advanced, split, recovery, *args, **kwargs)
        self.login_details = configuration.get_login_details()

    def start_requests(self):
        yield scrapy.FormRequest(url=self.login_details['login_url'],
                                 headers=self.login_details['headers'],
                                 meta={
                                     'dont_redirect': True,
                                     'handle_httpstatus_list': [302]
                                 },
                                 formdata={
                                     'Username': self.login_details['username'],
                                     'Password': self.login_details['password'],
                                     'RememberMe': self.login_details['remember_me'],
                                     'NextPage': self.login_details['next_page']
                                 },
                                 callback=self.after_login,
                                 dont_filter=False)

    def after_login(self, response):
        cookie = None
        for cookie_item in response.headers.getlist('Set-Cookie'):
            cookie = str(cookie_item).split(';')[0].split('session_0=')[1]
            if cookie != '':
                break
        session_cookies = {'session_0': cookie}
        if cookie == '':
            raise Exception('BNA Spider: Problem trying to logging in (Cookie not found)')
        else:
            yield scrapy.Request(self.searches[0]["url"], meta={"search": self.searches[0]},
                                 cookies=session_cookies)

    def get_session_cookies(self, response):
        cookie_str = str(response.request.headers.getlist('Cookie')[0]).split(';')[0].split('session_0=')[1]
        return {'session_0': cookie_str}

    def parse_details(self, url, cookies):
        link = url.split('bl')[1]
        ocr_text = get_ocr_bna(url, self.login_details, cookies)
        if ocr_text is None:
            ocr_text = ''
        download_url = 'https://www.britishnewspaperarchive.co.uk/viewer/download/bl' + link
        return download_url, ocr_text

    def create_recovery_file(self, last_search, next_page, row, last_date_partition):
        with open('recovery', 'w+') as page_err:
            values = [str(row + self.start_from_row),
                      str(last_search),
                      "False",
                      str(self.advanced),
                      next_page,
                      str(self.split),
                      str(last_date_partition)]
            separator = '\n'
            page_err.write(separator.join(values))

    def __str__(self):
        return "Spider details: " + json.dumps({
            'name': self.name,
            'allowed domains': self.allowed_domains,
            'search_url': self.search_url,
            'mode': 'slow',
            'search': 'advanced' if self.advanced else 'basic',
            'split': self.split
        }, indent=2)


class BNACountSpider(GeneralBNASpider):
    name = "BNACounting"

    def get_archive_search(self, search):
        if isinstance(search, AdvancedSearchTerms):
            return ArchiveSearchCount(archive=self.site_name,
                                      search_text=search.get_basic_search_string(),
                                      archive_date_start=search.start_date if search.start_date is not None else '',
                                      archive_date_end=search.end_date if search.end_date is not None else '',
                                      search_batch_id=self.name,
                                      added_date_start=search.added_start_date,
                                      added_date_end=search.added_end_date,
                                      article_type=search.article_type,
                                      exact_phrase=search.exact_phrase,
                                      exact_search=search.exact_search,
                                      exclude_words=search.exclude_words,
                                      front_page=search.front_page,
                                      newspaper_title=search.newspaper_title,
                                      publication_place=search.publication_place,
                                      search_all_words=search.all_words,
                                      sort_by=search.sort_by,
                                      tags=search.tags)
        else:
            return ArchiveSearchCount(archive=self.site_name,
                                      search_text=search.search_text,
                                      archive_date_start=search.start_date,
                                      archive_date_end=search.end_date,
                                      search_batch_id=self.name)

    def start_requests(self):
        for search in self.searches:
            yield scrapy.Request(search["url"], meta={"search": search})

    def parse(self, response, **kwargs):
        current_index = self.n_search
        self.n_search += 1
        resp = self.count_articles(response)
        resp["search_index"] = current_index
        yield resp
