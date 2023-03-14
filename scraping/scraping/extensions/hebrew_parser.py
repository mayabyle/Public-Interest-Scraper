from nltk.corpus import stopwords
import pandas as pd

def get_stop_words():
    words = set(stopwords.words('hebrew'))
    stop_words = []
    for word in words:
        stop_words.append(word)
        stop_words.append("ו"+"word")
        stop_words.append("ה"+word)
    return stop_words


def get_most_common_words_from_comments(conn):
    df = pd.read_sql_query("SELECT comment_text from ynet_comments", conn)
    stop_words = get_stop_words()
    print(stop_words)
    word_counts = (df['comment_text'].str.split(expand=True)  # split into words
                        .stack()  # stack the resulting columns
                        .apply(lambda x: x.strip())  # strip whitespace from each word
                        .where(lambda x: ~x.isin(stop_words))  # exclude stop words
                        .dropna()  # drop null values
                        .value_counts()  # count the occurrences of each word
                        .idxmax())  # get the index of the maximum value (i.e., the most common word)
    print(word_counts)