from __future__ import division

__author__ = 'linanqiu'


def rank_words(all_lines):
    raw_tf = {}
    df = {}

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
    beta = 0.075 * d
    alpha = 0.15 * d / beta
    loc = 0

    # print alpha
    # print beta
    # print loc

    from scipy.stats import gamma
    rv = gamma(a=alpha, loc=loc, scale=beta)
    # import matplotlib.pyplot as plt
    # import numpy as np
    # x = np.linspace(0, 2400)
    # plt.plot(x, rv.pdf(x))
    # plt.show()

    tfidf = []

    import math

    for word in df.keys():
        idf = rv.pdf(df[word])
        tf = math.log(raw_tf[word]) + 1
        tfidf.append({'word': word, 'tfidf': tf * idf, 'idf': idf, 'tf': tf, 'raw_tf': raw_tf[word], 'df': df[word]})

    sorted_tfidf = sorted(tfidf, key=lambda k: k['tfidf'], reverse=True)

    import simplejson
    f = open('words-gamma.json', 'wb')
    simplejson.dump(sorted_tfidf, f)
    f.close()

    # print sorted_tfidf[0]

    import csv
    keys = sorted_tfidf[0].keys()
    with open('words-gamma.csv', 'wb') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(sorted_tfidf)

    return sorted_tfidf

    # import cPickle as pickle
    # all_lines = pickle.load(open('all_lines', 'rb'))
    # rank_words(all_lines)
