import csv
import re


class WordCounter:

    def __init__(self, pos_filename, neg_filename):
        self.pos_file = open(pos_filename)
        self.neg_file = open(neg_filename)
        self.pos_dict = {}  # dictionary to map words from all positive reviews and its frequency
        self.neg_dict = {}  # dictionary to map words from all negative reviews and its frequency
        self.vocab = set()  # a set of unique words from training data(both pos and neg).
        self.pos_vocab = set()
        self.neg_vocab = set()

    @staticmethod
    def text_parser(text):
        parsed = re.split(r'[^\w]', text)
        return [w for w in parsed if w != '']

    def create_vocab_dict(self):
        """
        Use csv.reader to read files.
        row[2] corresponds to column['review'].
        """
        pos_reader = csv.reader(self.pos_file)
        neg_reader = csv.reader(self.neg_file)
        next(pos_reader)
        next(neg_reader)

        for row in pos_reader:
            wordlist = self.text_parser(row[2])
            single_review_vocab = set(wordlist)
            for word in single_review_vocab:
                self.vocab.add(word)
                self.pos_vocab.add(word)
                self.pos_dict[word] = self.pos_dict.get(word, 0) + 1

        for row in neg_reader:
            wordlist = self.text_parser(row[2])
            single_review_vocab = set(wordlist)
            for word in single_review_vocab:
                self.vocab.add(word)
                self.neg_vocab.add(word)
                self.neg_dict[word] = self.neg_dict.get(word, 0) + 1


test = WordCounter("./pos_train.csv", "./neg_train.csv")
test.create_vocab_dict()
print(test.pos_dict)
print("****************************************************************************************")
print(test.neg_dict)
