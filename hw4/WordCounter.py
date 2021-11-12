import csv
import math
import re


class WordCounter:

    def __init__(self, pos_filename, neg_filename):
        self.pos_file = open(pos_filename)
        self.neg_file = open(neg_filename)
        self.pos_dict = {}  # dictionary to map words from all positive reviews and its frequency
        self.neg_dict = {}  # dictionary to map words from all negative reviews and its frequency
        self.freq_dict = {}  # dictionary to map words from dataset(both pos and neg) and its frequency
        self.vocab = set()  # a set of unique words from dataset(both pos and neg).
        self.pos_vocab = set()  # a set of unique words from positive reviews.
        self.neg_vocab = set()  # a set of unique words from negative reviews.
        self.pos_review_num = 0  # positive review number
        self.neg_review_num = 0  # negative review number

    @staticmethod
    def text_parser(text):
        parsed = re.split(r'[^\w]', text)
        return [w for w in parsed if w != '']

    def prepare_data(self):
        """
        Use csv.reader to read files.  Row[2] corresponds to column['review'].
        Create vocab set for whole dataset, positive reviews and negative reviews respectively.
        Count positive review number and negative review number.
        Create dictionaries mapping word to its frequency.
        """
        pos_reader = csv.reader(self.pos_file)
        neg_reader = csv.reader(self.neg_file)
        next(pos_reader)
        next(neg_reader)

        for row in pos_reader:
            wordlist = self.text_parser(row[2])
            single_review_vocab = set(wordlist)
            self.pos_review_num += 1
            for word in single_review_vocab:
                self.vocab.add(word)
                self.pos_vocab.add(word)
                self.pos_dict[word] = self.pos_dict.get(word, 0) + 1
                self.freq_dict[word] = self.freq_dict.get(word, 0) + 1

        for row in neg_reader:
            wordlist = self.text_parser(row[2])
            single_review_vocab = set(wordlist)
            self.neg_review_num += 1
            for word in single_review_vocab:
                self.vocab.add(word)
                self.neg_vocab.add(word)
                self.neg_dict[word] = self.neg_dict.get(word, 0) + 1
                self.freq_dict[word] = self.freq_dict.get(word, 0) + 1


def get_freq(pos_dict, neg_dict, curr_word):
    f_word_pos = pos_dict.get(curr_word)
    f_word_neg = neg_dict.get(curr_word)


def mutual_info(_fxy, _N, _fx, _fy):
    a = _fxy * _N / (_fx * _fy)
    m_info = math.log(a, 2)
    return m_info



# test = WordCounter("./try.csv", "./try.csv")
test = WordCounter("./pos_train.csv", "./neg_train.csv")
test.prepare_data()



abs_mi = {}
for word in test.vocab:
    if test.pos_dict.get(word) == None:
        continue
    else:
        f_word_pos = test.pos_dict.get(word)

    if test.neg_dict.get(word) == None:
        continue
    else:
        f_word_neg = test.neg_dict.get(word)

    num = f_word_pos/f_word_neg

    a_mi = math.log(num, 2)
    abs_mi.update({word: a_mi})

sorted_abs_mi = sorted(abs_mi.items(), key=lambda x: x[1], reverse=True)

picked_freqs = [feature for feature in sorted_abs_mi if feature[1]>0]


features = list()
for feature in picked_freqs:
    features.append(feature[0])


mi_dict_pos = {}
for word in features:
    if test.pos_dict.get(word) == None:
        continue
    else:
        fxy = test.pos_dict.get(word)

    N = test.neg_review_num + test.pos_review_num
    fx = test.freq_dict.get(word)
    fy = test.pos_review_num
    #print(f'fxy {fxy}  fx  {fx}  fy {fy}  N {N}')
    mi = mutual_info(fxy, N, fx, fy)
    mi_dict_pos.update({word: mi})

# print(mi_dict_pos)
print(sorted(mi_dict_pos.items(), key=lambda x: x[1], reverse=True)[:5])





