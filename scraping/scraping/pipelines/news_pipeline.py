from itemadapter import ItemAdapter
import sqlite3
from ..items import ArticleItem, TagItem


class SqliteNoDuplicatesPipeline:

    def __init__(self):
        self.conn = sqlite3.connect('news.db')
        self.curr = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS articles(
                    source      TEXT,
                    subject     TEXT,
                    url         TEXT        PRIMARY KEY,
                    title       TEXT,
                    date        DATE,
                    comments    INTEGER,
                    tags        TEXT
                    )""")
        self.curr.execute("""CREATE TABLE IF NOT EXISTS tags(
                    url         TEXT,
                    date        DATE,
                    tag         TEXT,
                    UNIQUE(url, tag)
                    )""")
        self.curr.execute("""CREATE TABLE IF NOT EXISTS ynet_comments(
                            id                  INTEGER,
                            article_title       TEXT,
                            comment_headline    TEXT,
                            comment_text        TEXT,
                            likes               INTEGER,
                            unlikes             INTEGER,
                            UNIQUE(id, article_title)
                            )""")

    ## todo i made changes - to make sure there are no duplicates
    def process_item(self, item, spider):
        if isinstance(item, ArticleItem):
            self.curr.execute("""INSERT OR IGNORE INTO articles (source, subject, url, title, date, comments, tags)
                                VALUES (?,?,?,?,?,?,?)""", (
                item['source'],
                item['subject'],
                item['url'],
                item['title'],
                item['date'],
                item['comments_num'],
                ', '.join(item['tags'])))

            for tag in item['tags']:
                self.curr.execute("INSERT OR IGNORE INTO tags (url, date, tag) VALUES (?,?,?)",
                                  (item['url'], item['date'], tag))

            for comment in item['comments']:
                self.curr.execute("""INSERT OR IGNORE INTO ynet_comments (id, article_title, comment_headline, comment_text, likes, unlikes)
                                    VALUES (?,?,?,?,?,?)""",
                                  (comment['id'],
                                   item['title'],
                                   comment['title'],
                                   comment['text'],
                                   comment['likes'],
                                   comment['unlikes']))
            self.conn.commit()

        if isinstance(item, TagItem):
            self.curr.execute(
                "INSERT OR IGNORE INTO tags (url, date, tag) VALUES (?,?,?)",
                (item['url'], item['date'], item['search_tag']))
            self.conn.commit()

        return item
