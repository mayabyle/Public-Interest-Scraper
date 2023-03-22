from nltk.corpus import stopwords
import pandas as pd
import json
import time
import requests
from collections import defaultdict

stop_words = set(stopwords.words('hebrew'))
lemmas_count = defaultdict(int)


def parse_comment(text):
    print(text)
    if text != '':
        text = text.replace(r'"', r'\"')  # Escape double quotes in JSON.
        url = 'https://www.langndata.com/api/heb_parser?token=40087187fe4b783201d46adb001035bb'
        _json = '{"data":"' + text + '"}'
        r = requests.post(url, data=_json.encode('utf-8'), headers={'Content-type': 'application/json; charset=utf-8'})
        for word in r.json()['lemmas'].split(" "):
            if word not in stop_words and len(word) > 1:
                lemmas_count[word] += 1


def get_most_common_words_from_comments(curr, num):
    # df = pd.read_sql_query("SELECT comment_text from ynet_comments", conn)
    curr.execute("""SELECT comment_headline, comment_text FROM ynet_comments""")
    results = curr.fetchall()
    for line in results:
        for i in range(len(line)):
            time.sleep(3)
            try:
                parse_comment(line[i])
            except:
                time.sleep(1)
    print(lemmas_count)

# word_counts = (df['comment_text'].str.split(expand=True)  # split into words
#                     .stack()  # stack the resulting columns
#                     .apply(lambda x: x.strip())  # strip whitespace from each word
#                     .where(lambda x: ~x.isin(stop_words))  # exclude stop words
#                     .dropna()  # drop null values
#                     .value_counts()  # count the occurrences of each word
#                     .idxmax())  # get the index of the maximum value (i.e., the most common word)
# print(word_counts)
