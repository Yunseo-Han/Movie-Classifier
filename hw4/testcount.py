import csv
import re
import pandas as pd
from nltk.corpus import stopwords
from pandas import read_csv
import math


def tokenize(text):
    """
    :param text: movie review from a .txt file
    :return: a list of meaningful words
    """
    text = text.lower()
    clean_words = re.split(r'[^\w]', text)
    stopwords_en = stopwords.words("english")  # remove the stopwords
    return [w for w in clean_words if w not in stopwords_en and w != '']


def get_unique_words(csvfile):
    """
    :param csvfile: the csv file
    :return: a set of unique words
    """
    unique = set()
    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip the header, i.e. "id, sentiment, review"
        for row in reader:
            wordlist = tokenize(row[2])
            for word in wordlist:
                unique.add(word)
    return unique


def convert_reviews_2d_array(csvfile):
    """
    :param csvfile: the csv file
    :return: a 2d array. [['words', 'from', 'review1'], ['words', 'from', 'review2'] ['words', 'from', 'review3']]
    """
    review_list = list()
    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip the header, i.e. "id, sentiment, review"
        for row in reader:
            wordlist = tokenize(row[2])
            review_list.append(wordlist)
    return review_list


def build_freqs(csvfile):
    """
    :param csvfile: the csvfile
    :return: a dictionary mapping each (word, sentiment) pair to its frequency.
            For example: {('great', 1): 4, ('comic', 0): 1}
    """
    freqs = {}
    data = read_csv(csvfile)
    sentiments = data['sentiment'].tolist()
    # print(sentiments)
    reviews = convert_reviews_2d_array(csvfile)
    # print(reviews)
    for sentiment, review in zip(sentiments, reviews):
        single_review_word = set(review)
        for word in single_review_word:
            pair = (word, sentiment)
            if pair in freqs:
                freqs[pair] += 1
            else:
                freqs[pair] = 1
    return freqs


def count_pos_review_num(csvfile):
    """
    :return: the number of all positive reviews
    """
    count = 0
    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[1] == '1':
                count += 1
    return count


def mutual_info(fxy, N, fx, fy):
    a = fxy * N / (fx * fy)
    m_info = math.log2(a)
    return m_info


def main():
    file = 'testtrain.csv'
    df = pd.read_csv(file)
    total_review_num = len(df)
    total_pos_num = count_pos_review_num(file)
    total_neg_num = total_review_num - total_pos_num
    
    unique_words = get_unique_words(file)
    pairdict = build_freqs(file)
    print(pairdict)


if __name__ == '__main__':
    main()

'''
count = 0
for word, sentiment in pairdict:
    if sentiment == 0 and word == 'great':
        count = pairdict[word, sentiment]
print(count)
'''

# sorted_dict_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
# sorted_dict_listfreq = sorted(listfreq.items(), key=lambda x: x[1], reverse=True)


# apply stemming
'''
lists = ['beautiful', 'beauty', 'happy','happiness','get', 'gets', 'Friday', 'sunflowers']
stemmer = PorterStemmer()
review_stem = []
for word in lists:
    stem_word = stemmer.stem(word)
    review_stem.append(stem_word)

print(review_stem)
'''
