__author__ = 'linanqiu'

import glob
import cPickle as pickle
import os
import csv


class Sentences(object):
    def __init__(self, dirname, prefix):
        self.prefix = prefix
        self.dirname = dirname

    def __iter__(self):
        corpus_files = glob.glob('%s%s*' % (self.dirname, self.prefix))
        for corpus_file in corpus_files:
            corpus_segment = pickle.load(open(corpus_file, 'r'))
            for line in corpus_segment:
                yield line


class OmegaRedSentences(object):
    def __init__(self, file_list, substitute, substitute_key):
        self.file_list = file_list
        self.substitute = substitute
        self.substitute_key = substitute_key

    def __iter__(self):
        for reddit_file in self.file_list:
            with open(reddit_file, 'rb') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    subreddit_meta = '%s_%s_%s_%s' % (row[3], row[2], row[5], row[4])

                    if self.substitute is not None and self.substitute in subreddit_meta:
                        words = [self.substitute_key[word] if word in self.substitute_key else word for word in
                                 row[0].split(' ')]
                        yield words
                    else:
                        yield row[0].split(' ')
