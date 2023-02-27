from itemadapter import ItemAdapter
import sqlite3


class SqliteNoDuplicatesPipeline:

    def __init__(self):
        self.conn = sqlite3.connect('ynet.db')
        self.curr = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS ynet(
                    url         TEXT,
                    title       TEXT,
                    date        TEXT,
                    comments    INTEGER
                    )""")
        self.curr.execute("""CREATE TABLE IF NOT EXISTS ynet_tags(
                    title       TEXT,
                    tag         TEXT
                    )""")

    def process_item(self, item, spider):
        self.curr.execute("select * from ynet where url = ?", (item['url'],))
        result = self.curr.fetchone()
        if result:
            spider.logger.warn("Item already in database: %s" % item['title'])
        else:
            self.curr.execute("""INSERT INTO ynet (url, title, date, comments) VALUES (?,?,?,?)""", (
                item['url'],
                item['title'],
                item['date'],
                item['comments']))
            for tag in item['tags']:
                self.curr.execute("INSERT INTO ynet_tags (title, tag) VALUES (?,?)",
                                  (item['title'], tag))
            self.conn.commit()
        return item
