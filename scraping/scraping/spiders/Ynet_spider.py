import urllib, scrapy, json, re, requests

from datetime import datetime, date, timedelta
from scrapy.utils.project import get_project_settings
from scrapy_splash import SplashRequest

from ..items import ArticleItem, TagItem


# tags = ["המהפכה המשפטית"]
with open('C:/CS Studies/scraptingProject/scraping/tags.txt', 'r', encoding='utf-8') as f:
    tags = f.readlines()
urls = []
for tag in tags:
    urls.append(f'https://ynet.co.il/topics/{tag}')


class YnetSpider(scrapy.Spider):
    name = "ynet"
    allowed_domains = ['www.ynet.co.il']
    start_urls = urls

    def parse(self, response):
        if response.status != 200:
            return
        item = TagItem()
        currTag = urllib.parse.unquote(response.url.split("/")[-1], encoding='utf-8')
        links = response.xpath('.//div[@class="slotTitle"]/a/@href').getall()
        dates = response.xpath('.//span[@class="dateView"]/text()')

        for i in range(len(links)):
            parsed_date = datetime.strptime(dates[i].get().strip(), '%d.%m.%y').date()
            if parsed_date <= datetime(2023, 3, 18).date():
                break
            yield response.follow(links[i], callback=self.parse_article)
            # add the url and searched tag to tables
            item['url'] = links[i]
            item['date'] = parsed_date
            item['search_tag'] = currTag
            yield item

        next_page = response.xpath('.//div[@class="linksSwitchPageNum"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        item = ArticleItem()
        item['source'] = 'Ynet'
        item['subject'] = response.css('ul li:last-child a::text').get()
        item['url'] = response.url
        item['title'] = response.css('h1.mainTitle::text').get()
        item['date'] = response.xpath('//span[@class="DateDisplay"]/@data-wcmdate').extract_first()[:10]
        item['tags'] = response.xpath('//div[@class="tagName"]/a/text()').getall()
        item['comments'] = self.load_comments(response)
        item['comments_num'] = 0 if not item['comments'] else item['comments'][0]['number'] ##
        yield item

    def load_comments(self, response):
        i = 1
        comments = []
        unique_name = response.url.split("/")[-1]
        headers = get_project_settings().get('YNET_COMMENTS_REQUEST_HEADERS').copy()  # Copy default headers
        headers['Referer'] = response.url

        while True:
            url = f"https://www.ynet.co.il/iphone/json/api/talkbacks/list/{unique_name}/end_to_start/{i}"
            r = requests.get(url, headers=headers)
            data = json.loads(r.content)
            comment_list = data['rss']['channel']['item']
            if len(comment_list) == 0:
                break
            for comment in comment_list:
                comments.append(comment)
            i = i + 1
        return comments
