import sqlite3
import matplotlib.pyplot as plt
from tabulate import tabulate
from collections import defaultdict


class db_reader:

    def get_top_commented_titles(self, curr, limit=10):
        curr.execute("""
            SELECT title, date, comments 
            FROM ynet 
            ORDER BY comments DESC 
            LIMIT ?
            """, (limit,))
        results = curr.fetchall()
        print(tabulate(results, headers=['Title', 'Date', 'Comments']))

    def get_tags_num(self, curr):
        curr.execute("""
            SELECT tag, COUNT(*) as count
            FROM ynet_tags
            GROUP BY tag
            """)
        results = curr.fetchall()

        filtered_res = [tup for tup in results if tup[1] > 3]
        tags = [tup[0][::-1] for tup in filtered_res]
        counts = [tup[1] for tup in filtered_res]
        plt.bar(tags, counts)
        plt.xlabel('Tags')
        plt.ylabel('Count')
        plt.title('tags count')
        plt.xticks(rotation=40)
        plt.show()

    def run(self):
        conn = sqlite3.connect('scraping/scraping/ynet.db')
        curr = conn.cursor()
        # avg = curr.execute("""SELECT AVG(comments) FROM ynet""")
        # print(avg.fetchall())
        self.get_top_commented_titles(curr, 10)
        # self.get_tags_num(curr)
        conn.close()
