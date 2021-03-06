import crochet
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.signalmanager import dispatcher


from Crawler.settings import settings
from Crawler.spiders.BNASpider import GeneralBNASpider, BNACountSpider, BNASpiderWithLogin
from Crawler.utils.search_terms import SearchTerms, AdvancedSearchTerms
from repositories import searches_repo, configuration

crawl_runner = CrawlerRunner(Settings(settings))
scrape_in_progress = False
count_in_progress = False

current_activity_info = {
    "search_terms": None,  # Her I save an array with the search terms of the current search
    "search_index": -1,
    "downloaded_articles": [],
    "total_articles": [],  # Increasing list of total articles for each search_term
    "scrapping": False
}

count_activity_info = {
    "search_terms": None,  # Her I save an array with the search terms of the current search
    "total_articles": [],  # Increasing list of total articles for each search_term
    "counting": False
}

bp = Blueprint('search', __name__)
CORS(bp)


@bp.route('/search', methods=("GET", "POST"))
def start_search():
    global scrape_in_progress
    global current_activity_info

    if not scrape_in_progress:
        if request.method == 'POST':
            print(f"{request.json}")
            mode = request.json["mode"]
            ocr = request.json["ocr"] if "ocr" in request.json else False
            split = request.json["split"] if "split" in request.json else False
            print(mode == "advanced")
            input_search_terms = request.json["terms"]
            search_terms = get_search_terms_instances(input_search_terms, mode == 'advanced')
            login_details = None
            if ocr:
                login_details = configuration.get_login_details()
            scrape_with_crochet(configuration.db_variables(), mode == "advanced", search_terms, ocr, split,
                                login_details)
            current_activity_info = {"search_terms": input_search_terms, "search_index": 0, "downloaded_articles": [],
                                     "total_articles": [], "scrapping": True}
            scrape_in_progress = True
        return jsonify(current_activity_info)
    return jsonify(current_activity_info)


@bp.route('/search/stop', methods=("POST",))
def stop_search():
    global scrape_in_progress
    global current_activity_info
    scrape_in_progress = False
    current_activity_info["scrapping"] = False
    crawl_runner.stop()


def get_search_terms_instances(dict_search_terms, advanced):
    search_terms = []
    if not advanced:
        for ist in dict_search_terms:
            search_terms.append(SearchTerms(ist["keyword"],
                                            ist["start_date"],
                                            ist["end_date"]))
    else:
        for ist in dict_search_terms:
            # def __init__(self, start_date=None, end_date=None, added_start_date=None, added_end_date=None,
            #              article_type=None, exact_phrase=None, exact_search=None, exclude_words=None, front_page=None,
            #              newspaper_title=None, publication_place=None, all_words=None, some_words=None, sort_by=None,
            #              tags=None,
            #              timestamp=None):
            ast = AdvancedSearchTerms(
                start_date=ist["fromDate"],
                end_date=ist["toDate"],
                added_start_date=ist['fromDateAddedToSystem'],
                added_end_date=ist['toDateAddedToSystem'],
                article_type=ist['articleType'],
                exact_phrase=ist['useExactPhrase'],
                exact_search=ist["exactSearch"],
                exclude_words=ist['excludeWords'],
                front_page=ist['frontPageArticlesOnly'],
                newspaper_title=ist['newspaperTitle'],
                publication_place=ist['publicationPlace'],
                all_words=ist['searchAllWords'],
                some_words=ist['searchSomeWords'],
                sort_by=ist['sortResultsBy'],
                tags=ist['tags']
            )
            search_terms.append(ast)
    return search_terms


@bp.route('/search/download/status')
def download_status():
    return jsonify(current_activity_info)


@crochet.run_in_reactor
def scrape_with_crochet(db_vars, advanced, search_terms, ocr, split=None, login_details=None):
    current_activity_info["scrapping"] = True
    dispatcher.connect(_item_scraped, signal=signals.item_scraped)
    if ocr:
        eventual = crawl_runner.crawl(BNASpiderWithLogin, db_vars=db_vars, login_details=login_details, advanced=advanced,
                                      search_terms=search_terms, split=split)
    else:
        eventual = crawl_runner.crawl(GeneralBNASpider, db_vars=db_vars, advanced=advanced, search_terms=search_terms, split=split)
    eventual.addCallback(finished_scrape)


def finished_scrape(*args):
    """
    A callback that is fired after the scrape has completed.
    Set a flag to allow display the results from /results
    """
    global scrape_in_progress
    global current_activity_info
    scrape_in_progress = False
    current_activity_info["scrapping"] = False


def _item_scraped(item, response, spider):
    global current_activity_info
    current_activity_info["search_index"] = item["search_index"]
    current_activity_info["search_terms"] = spider.derived_search_terms
    if item["search_index"] >= len(current_activity_info["total_articles"]):
        for _ in range(item["search_index"] - len(current_activity_info["total_articles"]) ):
            current_activity_info["total_articles"].append(0)
            current_activity_info["downloaded_articles"].append(0)
        current_activity_info["total_articles"].append(item["total_articles"])
        current_activity_info["downloaded_articles"].append(0)
    current_activity_info["downloaded_articles"][-1] += 1


# ---------------------- COUNT ----------------------#
@bp.route('/search/count', methods=("GET", "POST"))
def start_count():
    global count_in_progress
    global count_activity_info

    if not count_in_progress:
        if request.method == 'POST':
            print(f"{request.json}")
            mode = request.json["mode"]
            print(mode == "advanced")
            input_search_terms = request.json["terms"]
            split = request.json["split"] if "split" in request.json else False
            search_terms = get_search_terms_instances(input_search_terms, mode == 'advanced')
            count_with_crochet(configuration.db_variables(), mode == "advanced", search_terms, split)
            count_activity_info = {
                "search_terms": input_search_terms,
                "total_articles": [],
                "counting": True
            }
            count_in_progress = True
        return jsonify(count_activity_info)
    return jsonify(count_activity_info)


@crochet.run_in_reactor
def count_with_crochet(db_vars, advanced, search_terms, split):
    dispatcher.connect(_item_counted, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(BNACountSpider, db_vars=db_vars, advanced=advanced, search_terms=search_terms, split=split)
    eventual.addCallback(finished_count)


def finished_count(*args):
    """
    A callback that is fired after the scrape has completed.
    Set a flag to allow display the results from /results
    """
    global count_in_progress
    global count_activity_info
    count_in_progress = False
    count_activity_info["counting"] = False


def _item_counted(item, response, spider):
    global count_activity_info
    count_activity_info["search_terms"] = spider.derived_search_terms
    if item["search_index"] >= len(count_activity_info["total_articles"]):
        count_activity_info["total_articles"].append(item["search_count"])


# ------------------------- SEARCH RESULTS ----------------------- #
@bp.route('/search/results')
def get_searches():
    print(request.args)
    limit = int(request.args.get("limit")) if request.args.get("limit") is not None else 10
    page = int(request.args.get("page")) - 1 if request.args.get("page") is not None else 0
    sortBy = request.args.get("sortby")  # posible values: id, from date, to date, keyword, time
    sortDesc = int(request.args.get("desc")) if request.args.get("desc") is not None else 0  # 1 or 0
    results, total = searches_repo.get_searches(limit, page, sortBy, sortDesc, configuration.db_variables())
    return jsonify({"results": results, "total": total})


@bp.route('/search/count/results')
def get_searches_count():
    print(request.args)
    limit = int(request.args.get("limit")) if request.args.get("limit") is not None else 10
    page = int(request.args.get("page")) - 1 if request.args.get("page") is not None else 0
    sortBy = request.args.get("sortby")  # posible values: id, from date, to date, keyword, time
    sortDesc = int(request.args.get("desc")) if request.args.get("desc") is not None else 0  # 1 or 0
    results, total = searches_repo.get_searches_count(limit, page, sortBy, sortDesc, configuration.db_variables())
    return jsonify({"results": results, "total": total})

