from scrapy.item import Item, Field


class ScrapingItem(Item):
    source = Field()
    url = Field()
    title = Field()
    date = Field()
    tags = Field()
    comments_num = Field()
    comments = Field()
