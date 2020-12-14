import crochet
from flask import Blueprint, request, render_template
from scrapy.crawler import CrawlerRunner
from Crawler.spiders.BNASpider import GeneralBNASpider
from Crawler.utils.search_terms import SearchTerms
from Crawler.settings import settings
from scrapy.settings import Settings

crawl_runner = CrawlerRunner(Settings(settings))
scrape_in_progress = False
scrape_complete = False

bp = Blueprint('setup', __name__, url_prefix='/setup')


@bp.route('/')
def start_search():
    return render_template('search/basicsearch.html')


@crochet.run_in_reactor
def scrape_with_crochet(search_terms):
    eventual = crawl_runner.crawl(GeneralBNASpider, search_terms=search_terms)
    eventual.addCallback(finished_scrape)


def finished_scrape(null):
    """
    A callback that is fired after the scrape has completed.
    Set a flag to allow display the results from /results
    """
    global scrape_complete
    scrape_complete = True
