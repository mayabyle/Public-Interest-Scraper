import os
import scraper_helper as sh

BOT_NAME = "scraping"

SPIDER_MODULES = ["scraping.spiders"]
NEWSPIDER_MODULE = "scraping.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Chrome/40.1"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DEFAULT_YNET_REQUEST_HEADERS = sh.get_dict('''
   accept: application/json, text/plain, */*,
   accept-language: he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7,
   cache-control: no-cache,
   pragma: no-cache,
   sec-ch-ua: "Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110",
   sec-ch-ua-mobile: ?0,
   sec-ch-ua-platform: "Windows",
   sec-fetch-dest: empty,
   sec-fetch-mode: cors,
   sec-fetch-site: same-origin,
   user-agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
''')

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "scraping.pipelines.ynet_pipeline.SqliteNoDuplicatesPipeline": 300,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "scraping.middlewares.ScrapingSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
#     'scrapy_proxies.RandomProxy': 410,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
# }
# # https://free-proxy-list.net/
# PROXY_LIST = os.path.join(os.getcwd(), 'C:\CS Studies\scraptingProject\proxy_list.txt')
# PROXY_MODE = 0

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"