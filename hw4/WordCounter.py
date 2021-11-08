import csv
import re
from itertools import islice


class WordCounter:

    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename)

    def fileIterator(self, isPos):
        if(isPos):
            reader = csv.reader(islice(self.file, start=2, stop=812))
        else:
            reader = csv.reader(islice(self.file, start=812, stop=None))

        for row in reader:
            # do something
            self.textParser(row[2])

    def textParser(text):
        parsed = re.split(r'[^\w]', text)
        return parsed

    def wordCounter(parsedText, word):
        counter = 0
        for e in parsedText:
            if e == word:
                counter += 1
