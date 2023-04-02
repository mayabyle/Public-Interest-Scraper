import sqlite3, requests, time
from nltk.corpus import stopwords
from collections import defaultdict

stop_words = set(stopwords.words('hebrew'))
lemmas_count = defaultdict(int)


def analyze_data(item, curr, conn):
    pass


def process_item(item, curr, conn):
    curr.execute("""INSERT OR IGNORE INTO words (word, date) VALUES (?,?)""", (
        item['source'],
        item['date']))
    conn.commit()


def parse_comment(conn, curr, text, date):
    print(text)
    if text != '':
        text = text.replace(r'"', r'\"')  # Escape double quotes in JSON.
        url = 'https://www.langndata.com/api/heb_parser?token=40087187fe4b783201d46adb001035bb'
        _json = '{"data":"' + text + '"}'
        r = requests.post(url, data=_json.encode('utf-8'), headers={'Content-type': 'application/json; charset=utf-8'})
        for word in r.json()['lemmas'].split(" "):
            if word not in stop_words and len(word) > 1:
                curr.execute("""INSERT OR IGNORE INTO words (word, date) VALUES (?,?)""", (
                    word,
                    date))
                conn.commit()
                # lemmas_count[word] += 1


# def get_most_common_words_from_comments(comments_curr, num):
#     # df = pd.read_sql_query("SELECT comment_text from ynet_comments", conn)
#     comments_curr.execute("""SELECT comment_headline, comment_text FROM ynet_comments""")
#     results = comments_curr.fetchall()
#     for line in results:
#         for i in range(len(line)):
#             time.sleep(3)
#             try:
#                 parse_comment(line[i])
#             except:
#                 time.sleep(1)
#     print(lemmas_count)


def parse(comments_curr, num):
    # Create SQL table:     todo add origin      TEXT,
    conn = sqlite3.connect('parsed_words.db')
    curr = conn.cursor()
    curr.execute("""CREATE TABLE IF NOT EXISTS words(
                    word        TEXT,
                    date        DATE
                    )""")

    # Parse comments and store in words table:
    comments_curr.execute("""
            SELECT articles.title, ynet_comments.comment_headline, ynet_comments.comment_text, articles.date
            FROM articles
            JOIN ynet_comments ON articles.title = ynet_comments.article_title""")
    results = comments_curr.fetchall()
    for line in results:
        date = line[3]
        for i in range(2):
            time.sleep(3)
            try:
                parse_comment(conn, curr, line[i + 1], date)
            except:
                time.sleep(1)
