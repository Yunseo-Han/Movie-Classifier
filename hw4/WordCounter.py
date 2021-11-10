import csv
import re
import copy
from itertools import islice


class WordCounter:

    def __init__(self, posFilename, negFilename):
        self.posfile = open(posFilename)
        self.negfile = open(negFilename)
        self.posdict = {}
        self.negdict = {}

    def createDict(self):
        posReader = csv.reader(self.posfile)
        negReader = csv.reader(self.negfile)

        words = []
        for row in islice(posReader, 2, None):
            # do something
            words += self.textParser(row[2])
        for row in islice(negReader, 2, None):
            # do something
            words += self.textParser(row[2])

        for word in words:
            self.posdict[word] = 0
        self.negdict = copy.deepcopy(self.posdict)

    def textParser(self, text):
        parsed = re.split(r'[^\w]', text)
        return parsed

    def wordCounter(self):
        posReader = csv.reader(self.posfile)
        negReader = csv.reader(self.negfile)

        for row in islice(posReader, 2, None):
            parsed = self.textParser(row[2])
            for word in parsed:
                if self.posdict.has_key(word):
                    self.posdict[word] += 1

        for row in islice(negReader, 2, None):
            parsed = self.textParser(row[2])
            for word in parsed:
                if self.negdict.has_key(word):
                    self.negdict[word] += 1


test = WordCounter("./pos_train.csv", "./neg_train.csv")
test.createDict()
print(test.posdict)
print("****************************************************************************************")
test.wordCounter()
print(test.posdict)
