# -*- coding: utf-8 -*-
import re
import json
from Crawler.utils.databasemodels import ArchiveSearchResult, CandidateDocument
from Crawler.utils import dbconn
import datetime
from items import ArticleItem
from Crawler.utils.dbutils import session_scope


class NewsPipeline(object):

    def process_item(self, item, spider):
        if spider.name == 'BNA':
            try:
                if spider.counting:
                    identifier = item["identifier"]
                    article_item = item["search_count"]
                    print 'Articles in search \"%s [%s - %s]\": %d' % (identifier, article_item.archive_date_start,
                                                                       article_item.archive_date_end,
                                                                       article_item.results_count)
                    with session_scope() as session:
                        dbconn.insert_search(session, article_item)
                else:
                    process_bna_item(item)
            except AttributeError:
                process_bna_item(item)

        elif spider.name == 'GN':
            articles_in_page_count = len(item['site'])
            for i in range(articles_in_page_count):
                site = item['site'][i]
                keyword = item['keyword'][i]
                reprint = item['reprints'][i]
                title = item['titles'][i]
                publish = item['publishs'][i]
                county = extract_county_from_bracket(item['counties'][i])
                word = item['words'][i]
                newspaper = item['newspapers'][i]
                download_page = item['download_pages'][i]

                article_item = ArticleItem(site=site, reprint=reprint, title=title, publish=publish,
                                           county=county, word=word, newspaper=newspaper, download_page=download_page)
                print 'Writting the data into the json file now..........'
                filename = site
                article_item.write_into_json_file(filename)

        elif spider.name == 'WNO':
            articles_in_page_count = len(item['site'])
            if articles_in_page_count > 0:
                site = item['site']
                keyword = item['keyword']
                start_date = item['start_date']
                end_date = item['end_date']
                search_id = item['search_id']
                filename = "{}_{}_{}_{}".format(site, keyword, start_date, end_date)
                for i in range(articles_in_page_count):
                    title = item['titles'][i]
                    title = extract_words_from_line_break(title)
                    publish = item['publishs'][i]
                    publish = extract_date_from_string(publish)
                    description = item['descriptions'][i]
                    description = extract_words_from_line_break(description)
                    # description = description.decode('unicode_escape')
                    type_ = extract_words_from_line_break(item['types'][i])
                    words = extract_number_from_string(item['words'][i])
                    newspaper = extract_words_from_line_break(item['newspapers'][i])
                    page = extract_number_from_string(item['pages'][i])
                    download_page = item['download_pages'][i]
                    ocr = extract_words_from_line_break(item['ocrs'][i])
                    article_item = ArticleItem(site=site, title=title, publish=publish,
                                               description=description, type_=type_, word=words, newspaper=newspaper,
                                               page=page, download_page=download_page, search_id=search_id,
                                               download_url=download_page, ocr=ocr, start_date=start_date,
                                               end_date=end_date)

                    print 'Writting the data into the json file now..........'
                    article_item.write_into_json_file(filename)
                    write_into_database(article_item, site='WNO')


def process_bna_item(page_item):
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
            title = extract_words_from_line_break(page_item['titles'][i])
            description = extract_words_from_line_break(page_item['descriptions'][i])
            hint = extract_words_from_hints(page_item['hints'][i])
            publish = page_item['publishs'][i]
            newspaper = extract_words_from_line_break(page_item['newspapers'][i])
            county = extract_words_from_line_break(page_item['counties'][i])
            type_ = extract_words_from_line_break(page_item['types'][i])
            word = extract_number_from_string(page_item['words'][i])
            page = extract_number_from_string(page_item['pages'][i])
            tag = extract_words_from_line_break(page_item['tags'][i])
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
            write_into_database(article_item, filename=filename)


def extract_words_from_hints(hints):
    p = re.compile('<[^>]+>')
    return p.sub("", hints)


def extract_words_from_line_break(string_):
    return string_.replace('\n', '').strip()


def extract_number_from_string(str_):
    return re.findall(r"\d+", str_)[0]


def extract_date_from_string(str_):
    return re.sub(r'\s+', '', str_).replace('Published:', '')


def extract_county_from_bracket(str_):
    # s = '(Edinburgh, Scotland),'
    words = re.match(r'.*\((.*)\).*', str_)
    if words is not None:
        return words.group(1)
    else:
        return None


def write_into_database(article_item, site='BNA', filename=None):
    publication_date = article_item["publish"]
    if site == 'BNA':
        publication_date = datetime.datetime.strptime(article_item["publish"], "%A %d %B %Y")
        publication_date = '{0.year:4d}-{0.month:02d}-{0.day:02d}'.format(publication_date)
    elif site == 'WNO':
        publication_date = article_item["publish"][:4].replace('st', '').replace('nd', '').replace('rd', '') \
            .replace('th', '')
        publication_date += article_item["publish"][4:]
        publication_date = datetime.datetime.strptime(publication_date, "%d%B%Y")
        publication_date = '{0.year:4d}-{0.month:02d}-{0.day:02d}'.format(publication_date)
        article_item["county"] = ""
    search_result = ArchiveSearchResult(title=article_item["title"].encode('latin-1', 'ignore'),
                                        url=article_item["download_url"].encode('latin-1', 'ignore'),
                                        description=article_item["description"].encode('latin-1', 'ignore'),
                                        publication_title=article_item["newspaper"].encode('latin-1', 'ignore'),
                                        publication_location=article_item["county"].encode('latin-1', 'ignore'),
                                        type=article_item["type_"].encode('latin-1', 'ignore'),
                                        archive_search_id=article_item["search_id"],
                                        publication_date=publication_date,
                                        word_count=article_item["word"])
    with session_scope() as session:
        dbconn.insert(session, search_result)
        unique_result = session.query(CandidateDocument.id) \
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
                    ocr = article_item["ocr"]
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


def write_into_json_file(article_item, filename):
    with open("Crawler/Records/" + filename + ".json", "a") as f:
        json.dump(article_item.__dict__, f)
        f.write(',\n')
