from __future__ import division

__author__ = 'linanqiu'

import logging

def same_meaning(substituted, original, word, n):
    return len(same_meaning_words(substituted, original, word, n))


def same_meaning_words(substituted, original, word, n):
    similar_substituted = set((word[0]) for word in substituted.most_similar(word, topn=n))
    similar_original = set((word[0]) for word in original.most_similar(word, topn=n))
    intersection = similar_substituted & similar_original
    return intersection


def generate_similarity_counts(original_model, substituted_model, intersect_vocab):

    logger = logging.getLogger('root')

    vocabs = {}

    count = 0
    for word in intersect_vocab:
        count += 1
        if count % 1000 == 0:
            logger.info('progress: %.2f' % (count / len(intersect_vocab)))
        similarity = same_meaning(substituted_model, original_model, word, 500)
        vocabs[word] = similarity

    return vocabs
