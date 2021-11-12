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
    reviews = convert_reviews_2d_array(csvfile)
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


def calc_fxy_fx(dictionary, curr_word, pos_or_neg):
    fxy = 0
    fx = 0

    flag = 1 if pos_or_neg == 'pos' else 0

    for word, sentiment in dictionary:
        if word == curr_word:
            fx += dictionary[word, sentiment]
        if sentiment == flag and word == curr_word:
            fxy = dictionary[word, sentiment]
    return fxy, fx


def calc_fxy_fx_neg(dictionary, curr_word):
    fxy = 0
    fx = 0
    for word, sentiment in dictionary:
        if word == curr_word:
            fx += dictionary[word, sentiment]
        if sentiment == 0 and word == curr_word:
            fxy = dictionary[word, sentiment]
    return fxy, fx


def mutual_info(fxy, N, fx, fy):
    a = fxy * N / (fx * fy)
    m_info = math.log(a, 2)
    return m_info


def main():
    file = 'train.csv'
    df = pd.read_csv(file)
    total_review_num = len(df)
    total_pos_num = count_pos_review_num(file)
    total_neg_num = total_review_num - total_pos_num
    vocab = get_unique_words(file)
    freq_dict = build_freqs(file)

    '''
    mi_dict = {}
    for word in vocab:
        fxy, fx = calc_fxy_fx_pos(freq_dict, word)
        if fxy == 0:
            continue
        N = total_review_num
        fy = total_pos_num
        mi = mutual_info(fxy, N, fx, fy)
        mi_dict.update({word: mi})
    '''
    abs_mi = {}
    for word in vocab:
        fxy, fx = calc_fxy_fx(freq_dict, word, "pos")
        if fxy == 0:
            continue
        N = total_review_num
        fy = total_pos_num
        mi_pos = mutual_info(fxy, N, fx, fy)

        fxy_neg, fx_neg = calc_fxy_fx(freq_dict, word, "neg")
        if fxy_neg == 0:
            continue
        fy = total_neg_num
        mi_neg = mutual_info(fxy_neg, N, fx_neg, fy)
        mi = abs(mi_pos - mi_neg)
        abs_mi.update({word: mi})

    sorted_dict_freq = sorted(abs_mi.items(), key=lambda x: x[1], reverse=True)
    print(sorted_dict_freq)


    '''
    sorted_dict_freq = sorted(mi_dict.items(), key=lambda x: x[1], reverse=True)
    
    with open('output.txt', 'w') as f:
        for key, value in sorted_dict_freq:
            f.write('%s:%s\n' % (key, value))
    '''




if __name__ == '__main__':
    main()





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
