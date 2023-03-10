from webbrowser import Chrome

import scrapy
from datetime import datetime, date, timedelta
from scrapy.utils.project import get_project_settings
from ..items import ScrapingItem
from scrapy_splash import SplashRequest


class N12Spider(scrapy.Spider):
    name = "N12"
    start_urls = ['https://www.mako.co.il/news-politics?page=1']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse, endpoint='render.html', args={'wait': 0.5})

    def parse(self, response):
        continue_page = True
        links = response.css('strong a::attr(href)').getall()
        dates = response.css('small span:last-child::text').getall()
        for i in range(len(links)):
            try:
                parsed_date = datetime.strptime(dates[i].strip(), '%d.%m.%y').date()
            except ValueError:
                parsed_date = date.today()
            delta = date.today() - parsed_date
            if delta > timedelta(days=0):
                continue_page = False
                continue
            links[i] = "http://www.mako.co.il"+links[i]
            yield SplashRequest(links[i], callback=self.parse_article, endpoint='render.html', args={'wait': 1})

        next_page = response.css('a.next::attr(href)').get()
        script = """function main(splash)
                    assert(splash:go(splash.args.url))
                    splash:wait(0.3)
                    button= splash:select("a[class=next]")"""
        if next_page is not None and continue_page:
            yield response.follow(next_page, callback=self.parse, endpoint='render.html')

    def parse_article(self, response):
        item = ScrapingItem()
        item['source'] = 'N12'
        item['url'] = response.url
        item['title'] = response.css('h1::text').get()
        item['date'] = response.css('span.display-date span:nth-child(1)::text').extract_first()[8:]
        item['tags'] = response.css('ul.tags a::text').getall()
        comments_str = response.css('.mako_comments__ammount::attr(data-amount)').get()
        if comments_str is not None and comments_str != '':
            item['comments_num'] = int(comments_str)
            item['comments'] = self.parse_comments(response)
        else:
            item['comments_num'] = 0
            item['comments'] = []
        yield item

    def parse_comments(self, response):
        comments = response.css('li.mklist__item.top_level_comment')
        print(len(comments))
        return []

#  docker pull scrapinghub/splash
# fetch('http://localhost:8050/render.html?url=https://www.mako.co.il/news-politics/legal_reforms/Article-50a162a6110c681026.htm?partner=lobby')