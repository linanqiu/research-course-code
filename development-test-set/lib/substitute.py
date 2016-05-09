from __future__ import division

__author__ = 'linanqiu'

import cPickle as pickle

import logging, os, sys
import sentences
import glob

logger = logging.getLogger('substitute')

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))


# def generate_substitute_key(sentences):
#     from tfidf.word_rank_gamma import rank_words
#
#     sorted_tfidf = rank_words(all_lines)
#
#     num_substitute = 100
#
#     selected_words = sorted_tfidf[:num_substitute]
#
#     substitute_key = {}
#
#     from random import shuffle
#
#     selected_words_shuffled = list(selected_words)
#     shuffle(selected_words_shuffled)
#
#     # print selected_words
#     # print selected_words_shuffled
#
#     for original_word, substituted_word in zip(selected_words, selected_words_shuffled):
#         substitute_key[original_word['word']] = substituted_word['word']
#
#     return substitute_key
#
#
# def generate_substitute_corpus(all_lines, substitute_key):
#     all_lines_substituted = []
#
#     for line in all_lines:
#         new_line = []
#         for word in line:
#             if (word in substitute_key):
#                 new_line.append(substitute_key[word])
#             else:
#                 new_line.append(word)
#
#         all_lines_substituted.append(new_line)
#
#     return all_lines_substituted
#
#
# import sentences

def generate_substitute_key_reddit(codeword_count, files):
    logger.info('Generating substitute key for reddit')
    sents = sentences.OmegaRedSentences(files, substitute=None, substitute_key=None)
    return generate_substitute_key(sents, codeword_count=codeword_count)


def generate_substitute_key_wsj(codeword_count):
    logger.info('Generating substitute key')
    os.getcwd()
    sents = sentences.Sentences(dirname='../data/', prefix='wsj_corpus')
    return generate_substitute_key(sents, codeword_count=codeword_count)


def generate_substitute_key(sents, codeword_count):
    sorted_tfidf = rank_words(sents)

    num_substitute = codeword_count

    selected_words = sorted_tfidf[:num_substitute]

    logger.info('Shuffling words')
    substitute_key = {}

    from random import shuffle

    selected_words_shuffled = list(selected_words)
    shuffle(selected_words_shuffled)

    for original_word, substituted_word in zip(selected_words, selected_words_shuffled):
        substitute_key[original_word['word']] = substituted_word['word']

    return (substitute_key, sorted_tfidf)


def write_substitute_key(substitute_key, sorted_tfidf, filename):
    logger.info('Writing substitute key')
    pickle.dump(substitute_key, open('./substitute_keys/%s.pkl' % filename, 'wb'))
    import simplejson

    f = open('./substitute_keys/%s.json' % filename, 'wb')
    simplejson.dump(substitute_key, f)
    f.close()

    f = open('./substitute_keys/%s_words_gamma.json' % filename, 'wb')
    simplejson.dump(sorted_tfidf, f)
    f.close()

    import csv
    keys = sorted_tfidf[0].keys()
    with open('./substitute_keys/%s_words_gamma.csv' % filename, 'wb') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(sorted_tfidf)


def rank_words(sents):
    logger.info('Ranking words')
    raw_tf = {}
    df = {}
    count = 0

    for line in sents:
        if count % 100000 == 0:
            logger.info('Ranking sentence %d' % count)
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
        count += 1

    d = count
    beta = 0.15 * d
    alpha = 0.15 * d / beta
    loc = 0

    import scipy.stats as stats
    rv = stats.gamma(a=alpha, loc=loc, scale=beta)

    tfidf = []

    import math

    for word in df.keys():
        idf = rv.pdf(df[word])
        tf = math.log(raw_tf[word]) + 1
        tfidf.append({'word': word, 'tfidf': tf * idf, 'idf': idf, 'tf': tf, 'raw_tf': raw_tf[word], 'df': df[word]})

    sorted_tfidf = sorted(tfidf, key=lambda k: k['tfidf'], reverse=True)

    return sorted_tfidf

# wsj_substitute_key, wsj_substitute_key_sorted_tfidf = generate_substitute_key_wsj(codeword_count=100)
# write_substitute_key(wsj_substitute_key, wsj_substitute_key_sorted_tfidf, 'wsj_substitute_key')
