import sqlite3
import matplotlib.pyplot as plt
# import hebrew_parser
from tabulate import tabulate

from scraping.scraping.extensions import hebrew_parser


def plot_topics_division(curr):
    curr.execute("""
                SELECT subject, COUNT(*) AS count
                FROM articles
                GROUP BY subject
                """)
    results = curr.fetchall()
    labels = [tup[0][::-1] for tup in results]
    sizes = [tup[1] for tup in results]
    # Plot
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.set_title('Distribution of subjects')
    plt.show()


def get_comments_avg(curr):
    avg1 = curr.execute("""SELECT AVG(comments) FROM articles WHERE source='Ynet'""")
    print("Ynet comments averge: ", avg1.fetchall())
    avg2 = curr.execute("""SELECT AVG(comments) FROM articles WHERE source='N12'""")
    print("N12 comments averge: ", avg2.fetchall())


def get_top_commented_titles(curr, limit):
    curr.execute("""
        SELECT title, date, comments, tags 
        FROM articles 
        ORDER BY comments DESC 
        LIMIT ?
        """, (limit,))
    results = curr.fetchall()
    print(tabulate(results, headers=['Title', 'Date', 'Comments']))


def get_tags_count(curr):
    curr.execute("""
            SELECT  P.week, P.tag, p.amount
            FROM    (SELECT tag, week, count(*) as amount
                    FROM        (SELECT tag, strftime('%W',date) week                                  
                                FROM tags AS t)  
                    group by tag, week) as P
                    
            JOIN 
            
            (SELECT tag, count(*) as amount
            FROM    (SELECT tag, strftime('%W',date) week                                  
                    FROM tags AS t)
            WHERE   week = strftime('%W',DATE('now'))
                    group by tag
                    order by amount desc
                    limit 5) 
            as filter on P.tag = filter.tag
            order by P.week, P.amount   
            """)
    results = curr.fetchall()
    print(results)
    # Plot MOST used tags from Ynet articles
    # filtered_res = [tup for tup in results if tup[1] > 3]
    # print(filtered_res)
    # tags = [tup[0][::-1] for tup in filtered_res]
    # counts = [tup[1] for tup in filtered_res]
    # plt.bar(tags, counts)
    # plt.xlabel('Tags')
    # plt.ylabel('Count')
    # plt.title('Top used tags in ynet')
    # plt.xticks(rotation=40)
    # plt.show()
    # # Plot LEAST used tags from Ynet articles
    # filtered_res = [tup for tup in results if tup[1] <= 2]
    # tags = [tup[0][::-1] for tup in filtered_res]
    # counts = [tup[1] for tup in filtered_res]
    # plt.bar(tags, counts)
    # plt.title('Least used tags in ynet')
    # plt.xticks(rotation=40)
    # plt.show()


def get_comments_data(curr, conn, num1, num2):
    # 5 most liked comments
    # curr.execute("""SELECT * FROM ynet_comments ORDER BY likes DESC LIMIT ?""", (num1,))
    # results = curr.fetchall()
    # print(tabulate(results, headers=['id', 'article', 'headline', 'text', 'likes', 'unlikes']))
    # most common words in comments (???)
    hebrew_parser.get_most_common_words_from_comments(curr, num2)




def run():
    conn = sqlite3.connect('scraping/news.db')
    curr = conn.cursor()
    # plot_topics_division(curr)
    # get_comments_avg(curr)
    # get_top_commented_titles(curr, 10)
    # get_tags_count(curr)
    get_comments_data(curr, conn, 5, 5)
    conn.close()







# period statistics reader

# def get_period_tags_count(curr):