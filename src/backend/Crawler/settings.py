# -*- coding: utf-8 -*-

# Scrapy settings for Crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

settings = {
"BOT_NAME": 'Crawler',

"SPIDER_MODULES": ['Crawler.spiders'],
"NEWSPIDER_MODULE": 'Crawler.spiders',

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT: 'Crawler (+http://www.yourdomain.com)'
"ITEM_PIPELINES": {
    'Crawler.pipelines.NewsPipeline': 300,
},
# Obey robots.txt rules
"ROBOTSTXT_OBEY": True,

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS: 1
"CONCURRENT_ITEMS": 16,
"DEPTH_PRIORITY": -100,
# SCHEDULER_DISK_QUEUE: 'scrapy.squeues.PickleFifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE: 'scrapy.squeues.FifoMemoryQueue'

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
"DOWNLOAD_DELAY": 0,
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN: 1
"CONCURRENT_REQUESTS_PER_IP": 16,

# Disable cookies (enabled by default)
"COOKIES_ENABLED": True,

# Disable Telnet Console (enabled by default)
"TELNETCONSOLE_ENABLED": True,
"TELNETCONSOLE_PORT": [6023, 6075],

# Override the default request headers:
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
# HTTPERROR_ALLOWED_CODES: 302
# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
"SPIDER_MIDDLEWARES": {
    # 'Crawler.middlewares.CrawlerSpiderMiddleware': 543,
    'Crawler.middlewares.RandomUserAgentMiddleware': 400
},

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES: {
#    'Crawler.middlewares.CrawlerDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
"EXTENSIONS": {
    'scrapy.extensions.telnet.TelnetConsole': 500,
},

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES: {
#    'Crawler.pipelines.CrawlerPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED: True
# The initial download delay
# AUTOTHROTTLE_START_DELAY: 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY: 20
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY: 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG: False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
"HTTPCACHE_ENABLED": True,
"HTTPCACHE_EXPIRATION_SECS": 3600,
# HTTPCACHE_DIR: 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES: []
# HTTPCACHE_STORAGE: 'scrapy.extensions.httpcache.FilesystemCacheStorage'

"LOG_LEVEL": 'ERROR'
}