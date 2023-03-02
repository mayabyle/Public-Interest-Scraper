from itemadapter import ItemAdapter
import sqlite3


class SqliteNoDuplicatesPipeline:

    def __init__(self):
        self.conn = sqlite3.connect('ynet.db')
        self.curr = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS ynet(
                    url         TEXT        PRIMARY KEY,
                    title       TEXT,
                    date        TEXT,
                    comments    INTEGER,
                    tags        TEXT
                    )""")
        self.curr.execute("""CREATE TABLE IF NOT EXISTS ynet_tags(
                    title       TEXT,
                    tag         TEXT
                    )""")
        self.curr.execute("""CREATE TABLE IF NOT EXISTS ynet_comments(
                            id                  INTEGER,
                            article_title       TEXT,
                            comment_headline    TEXT,
                            comment_text        TEXT,
                            likes               INTEGER,
                            unlikes             INTEGER
                            )""")

    def process_item(self, item, spider):
        self.curr.execute("select * from ynet where url = ?", (item['url'],))
        result = self.curr.fetchone()
        if result:
            spider.logger.warn("Item already in database: %s" % item['title'])
        else:
            self.curr.execute("""INSERT INTO ynet (url, title, date, comments, tags) VALUES (?,?,?,?,?)""", (
                item['url'],
                item['title'],
                item['date'],
                item['comments_num'],
                ', '.join(item['tags'])))

            for tag in item['tags']:
                self.curr.execute("INSERT INTO ynet_tags (title, tag) VALUES (?,?)",
                                  (item['title'], tag))

            for comment in item['comments']:
                self.curr.execute("""INSERT INTO ynet_comments (id, article_title, comment_headline, comment_text, likes, unlikes)
                                  VALUES (?,?,?,?,?,?)""",
                                  (comment['id'],
                                   item['title'],
                                   comment['title'],
                                   comment['text'],
                                   comment['likes'],
                                   comment['unlikes']))
            self.conn.commit()
        return item
