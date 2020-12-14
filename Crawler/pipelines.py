# -*- coding: utf-8 -*-
import re
import json
from Crawler.db.databasemodels import ArchiveSearchResult, CandidateDocument
from Crawler.db import dbconn
import datetime
from Crawler.items import ArticleItem
from Crawler.db.dbutils import session_scope


class NewsPipeline:

    def process_item(self, item, spider):
        try:
            if spider.name == 'BNACounting':
                identifier = item["identifier"]
                article_item = item["search_count"]
                c = article_item.results_count
                print(f'Articles in search "{identifier} [{article_item.archive_date_start} - '
                      f'{article_item.archive_date_end}]": {article_item.results_count}')
                with session_scope() as session:
                    dbconn.insert_search(session, article_item)
                return dict(search_index=item["search_index"], search_count=c)
            else:
                process_bna_item(item)
                return item
        except AttributeError:
            process_bna_item(item)
            return item


def process_bna_item(page_item):
    site = page_item['site']
    keyword = page_item['keyword']
    start_date = page_item['start_date']
    end_date = page_item['end_date']
    generate_json = page_item['generate_json']
    search_id = page_item['search_id']
    filename = "{}_{}_{}_{}".format(site, keyword, start_date, end_date)
    title = extract_words_from_line_break(page_item['title'])
    description = extract_words_from_line_break(page_item['description'])
    hint = extract_words_from_hints(page_item['hint'])
    publish = page_item['publish']
    newspaper = extract_words_from_line_break(page_item['newspaper'])
    county = extract_words_from_line_break(page_item['county'])
    type_ = extract_words_from_line_break(page_item['type'])
    word = extract_number_from_string(page_item['word'])
    page = extract_number_from_string(page_item['page'])
    tag = extract_words_from_line_break(page_item['tag'])
    download_page = page_item['download_page']
    download_url = page_item['download_url']
    ocr = page_item['ocr']

    article_item = ArticleItem(site=site, title=title, description=description,
                               hint=hint, publish=publish, newspaper=newspaper, county=county,
                               type_=type_, word=word, page=page, tag=tag, download_url=download_url,
                               download_page=download_page, ocr=ocr, start_date=start_date,
                               end_date=end_date, search_id=search_id)

    if generate_json:
        print('Writing data into the json file')
        article_item.write_into_json_file(filename)
    else:
        print('Writing data only into database')
        filename = None
    write_into_database(article_item)


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


def write_into_database(article_item, site='BNA'):
    publication_date = article_item["publish"]
    if site == 'BNA':
        publication_date = datetime.datetime.strptime(article_item["publish"], "%A %d %B %Y")
        publication_date = '{0.year:4d}-{0.month:02d}-{0.day:02d}'.format(publication_date)
    # elif site == 'WNO':
    #     publication_date = article_item["publish"][:4].replace('st', '').replace('nd', '').replace('rd', '') \
    #         .replace('th', '')
    #     publication_date += article_item["publish"][4:]
    #     publication_date = datetime.datetime.strptime(publication_date, "%d%B%Y")
    #     publication_date = '{0.year:4d}-{0.month:02d}-{0.day:02d}'.format(publication_date)
    #     article_item["county"] = ""
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
