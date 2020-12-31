from flask import Blueprint, request, jsonify, redirect, url_for
from scrapy.crawler import CrawlerRunner
from Crawler.settings import settings
from scrapy.settings import Settings
from repositories import configuration

crawl_runner = CrawlerRunner(Settings(settings))
scrape_in_progress = False
scrape_complete = False

bp = Blueprint('setup', __name__, url_prefix='/setup')


@bp.route('/bna', methods=("GET", "POST"))
def bna_details():
    if request.method == 'POST':
        print(request.json)
        configuration.set_bna_variables(**request.json)
        return redirect(url_for("setup.bna_details"))
    return jsonify(configuration.bna_variables())


@bp.route('/db', methods=("GET", "POST"))
def db_details():
    if request.method == 'POST':
        configuration.set_db_variables(**request.json)
        return redirect(url_for("setup.db_details"))
    return jsonify(configuration.db_variables())


@bp.route('/server', methods=("GET", "POST"))
def server_details():
    if request.method == 'POST':
        configuration.set_server_variables(**request.json)
        return redirect(url_for("setup.server_details"))
    return jsonify(configuration.server_variables())
