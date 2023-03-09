import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate
from nltk.corpus import stopwords


class db_reader:

    def get_comments_avg(self, curr):
        avg1 = curr.execute("""SELECT AVG(comments) FROM articles WHERE source='Ynet'""")
        print("Ynet comments averge: ", avg1.fetchall())
        avg2 = curr.execute("""SELECT AVG(comments) FROM articles WHERE source='N12'""")
        print("N12 comments averge: ", avg2.fetchall())

    def get_top_commented_titles(self, curr, limit):
        curr.execute("""
            SELECT title, date, comments, tags 
            FROM articles 
            ORDER BY comments DESC 
            LIMIT ?
            """, (limit,))
        results = curr.fetchall()
        print(tabulate(results, headers=['Title', 'Date', 'Comments']))

    def get_tags_count(self, curr):
        curr.execute("""
            SELECT tag, COUNT(*) as count
            FROM ynet_tags
            GROUP BY tag
            """)
        results = curr.fetchall()
        # Plot MOST used tags from Ynet articles
        filtered_res = [tup for tup in results if tup[1] > 3]
        print(filtered_res)
        tags = [tup[0][::-1] for tup in filtered_res]
        counts = [tup[1] for tup in filtered_res]
        plt.bar(tags, counts)
        plt.xlabel('Tags')
        plt.ylabel('Count')
        plt.title('Top used tags in ynet')
        plt.xticks(rotation=40)
        plt.show()
        # Plot LEAST used tags from Ynet articles
        filtered_res = [tup for tup in results if tup[1] <= 1]
        tags = [tup[0][::-1] for tup in filtered_res]
        counts = [tup[1] for tup in filtered_res]
        plt.bar(tags, counts)
        plt.title('Least used tags in ynet')
        plt.show()

    def get_comments_data(self, curr, conn):
        # 5 most liked comments
        curr.execute("""SELECT * FROM ynet_comments ORDER BY likes DESC LIMIT 5""")
        results = curr.fetchall()
        # print(tabulate(results, headers=['id', 'article', 'headline', 'text', 'likes', 'unlikes']))
        # most common words in comments
        df = pd.read_sql_query("SELECT comment_text from ynet_comments", conn)
        # define a set of stop words
        stop_words = set(stopwords.words('hebrew'))
        print(stop_words)
        # count the occurrences of each word, excluding stop words, and get the most common one
        word_counts = (df['comment_text'].str.lower()  # convert to lowercase
                            .str.split(expand=True)  # split into words
                            .stack()  # stack the resulting columns
                            .apply(lambda x: x.strip())  # strip whitespace from each word
                            .where(lambda x: ~x.isin(stop_words))  # exclude stop words
                            .dropna()  # drop null values
                            .value_counts()  # count the occurrences of each word
                            .idxmax()  # get the index of the maximum value (i.e., the most common word)
                            )
        # write the word counts to a CSV file
        print(word_counts)


    def run(self):
        conn = sqlite3.connect('scraping/scraping/news.db')
        curr = conn.cursor()
        # self.get_comments_avg(curr)
        # self.get_top_commented_titles(curr, 10)
        self.get_tags_count(curr)
        # self.get_comments_data(curr, conn)
        conn.close()
