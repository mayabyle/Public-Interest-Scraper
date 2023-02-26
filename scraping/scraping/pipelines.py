from itemadapter import ItemAdapter
import sqlite3


class ScrapingPipeline:

    def __init__(self):
        self.conn = sqlite3.connect('ynet.db')
        self.curr = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS ynet_tb(
                    url         TEXT,
                    title       TEXT,
                    date        TEXT,
                    comments    INT
                    )""")

    def process_item(self, item, spider):
        self.curr.execute("""INSERT INTO ynet_tb (url, title, date, comments) values (?,?,?,?)""",(
            item['url'],
            item['title'],
            item['date'],
            item['comments']
        ))
        ## Execute insert of data into database
        self.conn.commit()
        return item
