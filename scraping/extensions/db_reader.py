import sqlite3
import matplotlib.pyplot as plt

from collections import defaultdict
from tabulate import tabulate
from scraping.extensions import comments_parser

last_sunday = '2023-03-19'


def plot_week_topics_division(curr):
    curr.execute("""
                SELECT subject, COUNT(*) AS count, ()
                FROM articles
                WHERE date >= Date(?)
                GROUP BY subject
                """, (last_sunday,))
    results = curr.fetchall()
    print(results)
    for tup in results:
        print(tup[0], " ", tup[1])
    # Plot pie chart:
    # labels = [tup[0][::-1] for tup in results]
    # sizes = [tup[1] for tup in results]
    # fig, ax = plt.subplots()
    # ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    # ax.set_title('Distribution of subjects')
    # plt.show()


def get_comments_avg(curr):
    avg1 = curr.execute("""SELECT AVG(comments) 
                            FROM articles 
                            WHERE source='Ynet' AND date >= Date(?)"""
                        , (last_sunday,))
    print("Ynet comments average: ", avg1.fetchall())
    avg2 = curr.execute("""SELECT AVG(comments) 
                            FROM articles 
                            WHERE source='N12' AND date >= Date(?)"""
                        , (last_sunday,))
    print("N12 comments average: ", avg2.fetchall())


def get_top_commented_titles(curr, limit):
    curr.execute("""
        SELECT title, date, comments, tags 
        FROM articles 
        WHERE date >= Date(?)
        ORDER BY comments DESC 
        LIMIT ?""", (last_sunday, limit,))
    results = curr.fetchall()
    print(tabulate(results, headers=['Title', 'Date', 'Comments']))
    # Plot tags from popular articles chart:
    # tags_count = defaultdict(int) todo


def get_week_tags_count(curr):
    curr.execute("""SELECT tag, COUNT(*) AS count
                    FROM tags
                    WHERE date >= DATE(?)
                    GROUP BY tag
                    ORDER BY count DESC""", (last_sunday,))
    results = curr.fetchall()
    # Plot MOST used tags from Ynet articles chart:
    filtered_res = [tup for tup in results if tup[1] > 5 and tup[0] != 'המהפכה המשפטית']
    tags = [tup[0][::-1] for tup in filtered_res]
    counts = [tup[1] for tup in filtered_res]
    plt.bar(tags, counts)
    plt.xlabel('Tags')
    plt.ylabel('Count')
    plt.title('Top used tags in ynet')
    plt.xticks(rotation=40)
    plt.show()
    # Print LEAST used tags from Ynet articles
    least_used = [tup[0] for tup in results if tup[1] <= 4]
    print(least_used)


def get_period_tags_count(curr):
    curr.execute("""
            SELECT  P.week, P.tag, p.amount
            FROM    (SELECT tag, week, count(*) as amount
                    FROM        (SELECT tag, strftime('%W',date) week                                  
                                FROM tags)  
                    WHERE tag NOT IN ('0', '1')
                    group by tag, week) as P
                    
            JOIN 
            
            (SELECT tag, count(*) as amount
            FROM    (SELECT tag, strftime('%W',date) week                                  
                    FROM tags AS t)
            WHERE   week = strftime('%W',DATE('now')) 
            group by tag
            order by amount desc
            limit 5) as filter on P.tag = filter.tag
            order by P.week, P.tag   
            """)
    results = curr.fetchall()
    print(results)
    # Plot line chart:
    lines = {}
    for result in results:
        if lines.get(result[1][::-1]) is None:
            lines[result[1][::-1]] = []
        lines[result[1][::-1]].append((int(result[0]), result[2]))
    for line_name, line_data in lines.items():  # Plot each line
        line_data = sorted(line_data, key=lambda x: x[0])  # Sort the data by week
        x_axis, y_axis = zip(*line_data)  # extract x and y values from the tuples
        plt.plot(x_axis, y_axis, label=line_name)  # plot the line and add a label
    plt.legend()
    plt.title('Top used tags in ynet over the weeks')
    plt.xlabel('week')
    plt.ylabel('count')
    plt.show()


def get_comments_data(curr, num1, num2):
    # 5 most liked comments
    curr.execute("""SELECT * FROM ynet_comments 
            INNER JOIN articles
            ON ynet_comments.article_title = articles.title
            WHERE articles.date >= DATE(?)
            ORDER BY likes DESC LIMIT ?""", (last_sunday, num1,))
    results = curr.fetchall()
    for tup in results:
        print(tup[1])
        print(tup[2])
        print(tup[3])
        print(tup[4])
        print(tup[5])
        print("------------------")
    # most common words in comments
    # comments_parser.parse(curr, num2)


def run():
    conn = sqlite3.connect('news.db')
    curr = conn.cursor()
    # plot_week_topics_division(curr)
    # get_comments_avg(curr)
    # get_top_commented_titles(curr, 10)
    # get_week_tags_count(curr)
    # get_period_tags_count(curr)
    get_comments_data(curr, 5, 5)
    conn.close()
