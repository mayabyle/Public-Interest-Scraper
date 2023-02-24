from pathlib import Path

import scrapy


class YnetSpider(scrapy.Spider):
    name = "Ynet"
    start_urls = ['https://www.ynet.co.il/topics/המהפכה_המשפטית']

    # Scrapy’s default callback method
    def parse(self, response):
        article_list = response.css('div.slotView')
        # xpath() method used to extract the href attribute of the link within the div element with class="slotTitle"
        links = article_list.xpath('.//div[@class="slotTitle"]/a/@href')
        for link in links:
            yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        # extract the article content
        # article_content = response.css('div.article-body')[0].get()
        # extract the URL and use it to construct the filename
        url = response.url
        filename = f'{url.split("/")[-1]}.html'
        # write the content to a file with the unique filename
        Path(filename).write_bytes(response.body)

        # title = response.css('h1.articleTitle::text').get()
        # filename = f'ynet-{title}.html'
        # Path(filename).write_bytes(response.body)

#
#
# from pathlib import Path
#
# import scrapy
#
# tags = ["המהפכה המשפטית", "עילת הסבירות", ""]
#         # "", "", "", "", "", "",
#         # "", "", "", "", "", "", "", "", "", "", "",
#         # "", "", "", "", "", ""]
