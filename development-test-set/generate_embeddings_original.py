__author__ = 'linanqiu'

from w2v.w2v import *

import logging
import os.path
import sys

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))

all_lines_original_filename = 'corpus-original.pkl'
# all_lines_substituted_filename = 'corpus-substituted.pkl'

# from itertools import izip
# import cPickle as pickle
# all_lines_original = pickle.load(open(all_lines_original_filename, 'rb'))
# all_lines_substituted = pickle.load(open(all_lines_substituted_filename, 'rb'))
# for line_original, line_substituted in zip(all_lines_original, all_lines_substituted):
#     for word_original, word_substituted in zip(line_original, line_substituted):
#         if(word_original != word_substituted):
#             print "%s : %s" % (word_original, word_substituted)

all_lines_original = build_sentences(all_lines_original_filename)
# all_lines_substituted = build_sentences(all_lines_substituted_filename)

original_model = model_from_sentences(all_lines_original)
# substituted_model = model_from_sentences(all_lines_substituted)

original_model.save_word2vec_format('./models/corpus-original-w2v.mdl', binary=True)
# substituted_model.save_word2vec_format('./models/corpus-substituted-w2v.mdl', binary=True)

# original_model = model_from_saved("./models/corpus-original-w2v.mdl", binary=True)
# substituted_model = model_from_saved("./models/corpus-substituted-w2v.mdl", binary=True)
#
# print(original_model.most_similar('home'))
# print(substituted_model.most_similar('home'))
#
# def same_meaning(substituted, original, word, n):
#     return len(same_meaning_words(substituted, original, word, n))
#
# def same_meaning_words(substituted, original, word, n):
#     similar_substituted = set((word[0]) for word in substituted.most_similar(word, topn = n))
#     similar_original = set((word[0]) for word in original.most_similar(word, topn = n))
#     print(similar_substituted)
#     print(similar_original)
#     intersection = similar_substituted & similar_original
#     return intersection
#
# print(same_meaning(substituted_model, original_model, 'good', 10))
# print(same_meaning(substituted_model, original_model, 'finance', 10))
# print(same_meaning(substituted_model, original_model, 'office', 10))
