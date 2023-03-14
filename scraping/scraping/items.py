from scrapy.item import Item, Field


class ArticleItem(Item):
    source = Field()
    subject = Field()
    url = Field()
    title = Field()
    date = Field()
    tags = Field()
    comments_num = Field()
    comments = Field()


class TagItem(Item):
    url = Field()
    date = Field()
    search_tag = Field()
