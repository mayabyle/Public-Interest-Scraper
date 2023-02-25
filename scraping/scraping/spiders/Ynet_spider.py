from pathlib import Path
from datetime import datetime, date, timedelta
import scrapy

# tags = ["המהפכה המשפטית"]
tags = ["המהפכה המשפטית", "עילת הסבירות", "חוקה",
        "ביבי", "בנימין נתניהו", "עילת הסבירות", "הוועדה למינוי שופטים",
        "חוקים", "פסקת ההתגברות", "יריב לוין", "חוק דרעי",
        "רפורמה", "שמחה רוטמן", "זכויות נשים", "אפליה"]
urls = []
for tag in tags:
    urls.append(f'https://ynet.co.il/topics/{tag}')


class YnetSpider(scrapy.Spider):
    name = "Ynet"
    allowed_domains = ['www.ynet.co.il']
    start_urls = urls

    def parse(self, response):
        links = response.xpath('.//div[@class="slotTitle"]/a/@href')
        dates = response.xpath('.//span[@class="dateView"]/text()')
        for i in range(len(links)):
            parsed_date = datetime.strptime(dates[i].get().strip(), '%d.%m.%y').date()
            delta = date.today() - parsed_date
            if delta > timedelta(days=3):
                break
            yield response.follow(links[i], callback=self.parse_article)

        next_page = response.xpath('.//div[@class="linksSwitchPageNum"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        url = response.url
        filename = f'{url.split("/")[-1]}.html'
        Path(filename).write_bytes(response.body)
