# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from bs4 import BeautifulSoup
from Crawler.items import PageItem
import requests
import re
import scrapy
import json
import os
import csv
from DB.databasemodels import ArchiveSearch
import DB.dbconn
import bna_login_details as login


class BNASpider(Spider):

    name = "BNA"
    allowed_domains = ['britishnewspaperarchive.co.uk']

    search_url = 'https://www.britishnewspaperarchive.co.uk/search/results'
    login_url = "https://www.britishnewspaperarchive.co.uk/account/login"
    SITE_NAME = 'britishnewspaperarchive'
    search_key_words = []
    SLASH = '/'

    filename = 'Crawler/spiders/BNA_search_input.csv'

    if os.path.exists(filename):
        print 'BNA Spider: Reading BNA input file\n'
        with open(filename, 'rb') as csv_file:
            reader = csv.DictReader(csv_file)
            search_key_words = [row for row in reader]
    else:
        print 'BNA Spider: ' + filename + ' was not found. Check if it exists.'
    
    parse_urls = []
    search_db = []
    for i in range(len(search_key_words)):
        search_db.append(ArchiveSearch(archive="britishnewspaperarchive", search_text=search_key_words[i]['keyword'],
                                       archive_date_start=search_key_words[i]['start day(xxxx-xx-xx)'],
                                       archive_date_end=search_key_words[i]['end day(xxxx-xx-xx)'],
                                       search_batch_id="BNA"))
        parse_urls.append(search_url + SLASH + search_key_words[i]['start day(xxxx-xx-xx)'] + SLASH +
                          search_key_words[i]['end day(xxxx-xx-xx)'] + '?basicsearch=' + search_key_words[i]['keyword']
                          + '&retrievecountrycounts=false&page=0')

    @staticmethod
    def parse_next_page(response):
        data = response.body
        soup = BeautifulSoup(data, "html.parser", from_encoding="utf8")
        next_page = soup.find(name='a', attrs={'title': re.compile(r"Forward")})
        # print len(next_page)
        if next_page:
            return next_page['href']
        else:
            print 'Error'

    def start_requests(self):
        print 'BNA Spider: Logging in\n'
        return [scrapy.FormRequest(url=self.login_url,
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
                                   dont_filter=False
                                   )]

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
            for search in self.search_db:
                DB.dbconn.insert_search(search)
            count = 0
            for url in self.parse_urls:
                yield scrapy.Request(url, meta={"keyword_count": count},
                                     cookies=session_cookies)
                count = count + 1

    def parse(self, response):
        cookie_str = response.request.headers.getlist('Cookie')[0].split(';')[0].split('session_0=')[1]
        session_cookies = {'session_0': cookie_str}
        keyword_count = response.meta['keyword_count']
        print 'BNA Spider: Crawling ', self.search_key_words[int(keyword_count)]['keyword']

        page = PageItem()
        page['site'] = []
        page['keyword'] = []
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
        page['start_date'] = []
        page['end_date'] = []
        page['search_id'] = []

        data = response.body
        soup = BeautifulSoup(data, "html.parser", from_encoding="utf8")

        all_articles = soup.find_all("article", class_="bna-card")
        for article in all_articles:
            # To get the title text 
            this_title = article.find('h4', class_="bna-card__title")

            article_detail_url = response.urljoin(this_title.find('a').get('href'))
            page['download_pages'].append(article_detail_url)
            download_url, ocr = self.parse_details(article_detail_url, cookies=session_cookies)
            page['download_urls'].append(download_url)
            page['ocrs'].append(ocr)

            for title in this_title.stripped_strings:
                page['titles'].append(title)
                page['site'].append(self.SITE_NAME)
                page['keyword'].append(self.search_key_words[keyword_count]['keyword'])
                page['start_date'].append(self.search_key_words[keyword_count]['start day(xxxx-xx-xx)'])
                page['end_date'].append(self.search_key_words[keyword_count]['end day(xxxx-xx-xx)'])
                page['search_id'].append(self.search_db[keyword_count].id)

            # To get the title text title tag
            this_title = article.find('h4', class_="bna-card__title")
            title_tag = this_title.find('a')
            this_title_all_attributes = title_tag.attrs
            this_title_title_attribute = this_title_all_attributes['title']
            page['hints'].append(this_title_title_attribute)

        all_description = soup.find_all('p', class_="bna-card__body__description")
        for description in all_description:
            page['descriptions'].append(description.get_text())

        all_metas = soup.find_all('div', class_="bna-card__meta")
        for meta in all_metas:
            page['publishs'].append(meta.small.span.get_text())
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

        next_page = self.parse_next_page(response)
        if next_page is not None:
            next_page_full_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_full_url, meta={"keyword_count": keyword_count}, headers=login.headers)

    @staticmethod
    def parse_details(url, cookies):
        link = url.split('bl')[1]

        ocr_link = 'https://www.britishnewspaperarchive.co.uk/tags/itemocr/BL/' + link
        json_str = requests.get(ocr_link, cookies=cookies, headers=login.headers)
        json_str.encoding = 'gbk'
        json_str = json.loads(json_str.content)
        ocr_text = ''
        for j in json_str:
            ocr_text = ocr_text + j['LineText']
        # print OCR_text
        download_url = 'https://www.britishnewspaperarchive.co.uk/viewer/download/bl' + link
        return download_url, ocr_text
