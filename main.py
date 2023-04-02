from scraping.spiders.N12_spider import N12Spider
from scraping.spiders.Ynet_spider import YnetSpider
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scraping.extensions.db_reader import run


if __name__ == '__main__':
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(YnetSpider)
    process.crawl(N12Spider)
    process.start()

    reader = run()

