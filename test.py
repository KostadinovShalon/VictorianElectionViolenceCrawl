import scrapy
from scrapy.crawler import CrawlerProcess

from Crawler.spiders.BNASpider import BNASpider

settings = {
    "BOT_NAME": 'Crawler',

    "SPIDER_MODULES": ['Crawler.spiders'],
    "NEWSPIDER_MODULE": 'Crawler.spiders',

    "ITEM_PIPELINES": {
        'Crawler.pipelines.NewsPipeline': 300,
    },
    # Obey robots.txt rules
    "ROBOTSTXT_OBEY": True,

    "CONCURRENT_REQUESTS": 1,
    "CONCURRENT_ITEMS": 1,
    "DEPTH_PRIORITY": -100,

    "DOWNLOAD_DELAY": 0,

    "CONCURRENT_REQUESTS_PER_DOMAIN": 1,

    "COOKIES_ENABLED": True,

    "TELNETCONSOLE_ENABLED": True,
    "TELNETCONSOLE_PORT": [6023, 6075],

    "DEFAULT_REQUEST_HEADERS": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/64.0.3282.167 Safari/537.36 "
    },

    "USER_AGENT_LIST": [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 '
        'Safari/534.53.10 '
    ],

    "SPIDER_MIDDLEWARES": {
        # 'Crawler.middlewares.CrawlerSpiderMiddleware': 543,
        'Crawler.middlewares.RandomUserAgentMiddleware': 400
    },

    "EXTENSIONS": {
        'scrapy.extensions.telnet.TelnetConsole': 500,
    },

    "HTTPCACHE_ENABLED": True,
    "HTTPCACHE_EXPIRATION_SECS": 3600,

    "LOG_LEVEL": 'ERROR'

}

process = CrawlerProcess(settings=settings)
process.crawl(BNASpider, mode="fast")
process.start()
