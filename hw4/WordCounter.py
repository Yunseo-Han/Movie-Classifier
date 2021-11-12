import csv
import re


class WordCounter:

    def __init__(self, pos_filename, neg_filename):
        self.pos_file = open(pos_filename)
        self.neg_file = open(neg_filename)
        self.pos_dict = {}
        self.neg_dict = {}
        self.vocab = set()

    @staticmethod
    def text_parser(text):
        parsed = re.split(r'[^\w]', text)
        return [w for w in parsed if w != '']

    def create_vocab_dict(self):
        pos_reader = csv.reader(self.pos_file)
        neg_reader = csv.reader(self.neg_file)
        next(pos_reader)
        next(neg_reader)

        for row in pos_reader:
            wordlist = self.text_parser(row[2])
            for word in wordlist:
                self.vocab.add(word)
                self.pos_dict[word] = self.pos_dict.get(word, 0) + 1

        for row in neg_reader:
            wordlist = self.text_parser(row[2])
            for word in wordlist:
                self.vocab.add(word)
                self.neg_dict[word] = self.neg_dict.get(word, 0) + 1




test = WordCounter("./pos_train.csv", "./neg_train.csv")
test.create_vocab_dict()
print(test.pos_dict)
print("****************************************************************************************")
print(test.pos_dict)
