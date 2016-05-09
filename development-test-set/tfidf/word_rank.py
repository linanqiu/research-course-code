from __future__ import division

__author__ = 'linanqiu'

raw_tf = {}
df = {}

import cPickle as pickle

all_lines = pickle.load(open('all_lines', 'rb'))

count = 0
for line in all_lines:
    line_set = set(line)
    for word in line:
        if word in raw_tf:
            raw_tf[word] += 1
        else:
            raw_tf[word] = 1

    for word in line_set:
        if word in df:
            df[word] += 1
        else:
            df[word] = 1

d = len(all_lines)

tfidf = []

import math

for word in df.keys():
    idf = math.log(1 + (d / df[word]))
    tf = math.log(raw_tf[word]) + 1
    tfidf.append({'word': word, 'tfidf': tf * idf, 'idf': idf, 'tf': tf, 'raw_tf': raw_tf[word], 'df': df[word]})

sorted_tfidf = sorted(tfidf, key=lambda k:k['tfidf'], reverse=True)

import simplejson
f = open('words.json', 'wb')
simplejson.dump(sorted_tfidf, f)
f.close()

print sorted_tfidf[0]

import csv
keys = sorted_tfidf[0].keys()
with open('words.csv', 'wb') as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(sorted_tfidf)