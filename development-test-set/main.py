__author__ = 'linanqiu'

import logging
import os.path
import sys
import cPickle as pickle

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))


# reads wsj corpus and saves all lines to all-lines.pkl
logger.info('Reading WSJ corpus')
from lib.corpus_parser import *

all_lines = parse_wsj()
pickle.dump(all_lines, open('all-lines.pkl', 'wb'))

# generate substitute key
logger.info('Generating substitute key based on tfidf function chosen in lib.substitute')
from lib.substitute import *

substitute_key = generate_substitute_key(all_lines)
pickle.dump(substitute_key, open('substitute-key.pkl', 'wb'))
import simplejson

f = open('substitute-key.json', 'wb')
simplejson.dump(substitute_key, f)
f.close()

# substitute words in all lines using substitute key
logger.info('Substituting words in all lines using substitute key')
all_lines_substituted = generate_substitute_corpus(all_lines, substitute_key)
pickle.dump(all_lines_substituted, open('corpus-substituted.pkl', 'wb'))
# save original corpus too
pickle.dump(all_lines, open('corpus-original.pkl', 'wb'))

# run word2vec from gensim on original corpus and substituted corpus
logger.info('Running word2vec on original corpus and substituted corpus')
from w2v.w2v import *

all_lines_original = build_sentences('./models/corpus-original-w2v.mdl')
all_lines_substituted = build_sentences('./models/corpus-substituted-w2v.mdl')

original_model = model_from_sentences(all_lines_original)
substituted_model = model_from_sentences(all_lines_substituted)

original_model.save_word2vec_format('./models/corpus-original-w2v.mdl', binary=True)
substituted_model.save_word2vec_format('./models/corpus-substituted-w2v.mdl', binary=True)

# original_model = model_from_saved("./models/corpus-original-w2v.mdl", binary=True)
# substituted_model = model_from_saved("./models/corpus-substituted-w2v.mdl", binary=True)

# compare based on similarity
logger.info('Finding common vocabularies')
from comparison.similarity import *

intersect_vocab = set(substituted_model.vocab).intersection(set(original_model.vocab))
logger.info("%d words found" % len(intersect_vocab))


# generating similarity counts
logger.info('Generating similarity counts for all vocabs')
vocabs = generate_similarity_counts(original_model, substituted_model, intersect_vocab)
pickle.dump(vocabs, open('vocabs-compared.pkl', 'wb'))


# plot results
codewords = sorted(vocabs, key=vocabs.get)
positive = 0
false_positive = 0
count = 1
results = {}

for word in codewords:
    if word in substitute_key:
        positive += 1
    else:
        false_positive += 1
    results[count] = {'count': count, 'positive': positive, 'false_positive': false_positive,
                      'false_negative': len(substitute_key) - positive}
    count += 1

import pandas as pd
import matplotlib
import matplotlib.pyplot as plot

matplotlib.style.use('ggplot')

# distribution of comparison counts
plot.hist(vocabs.values(), bins=100)
plot.show()

# plot results
dataframe = pd.DataFrame.from_dict(results, orient='index')
dataframe.plot(x='count', y=['positive', 'false_positive', 'false_negative'], xlim=[0, 200], ylim=[0, 100])
plot.show()
