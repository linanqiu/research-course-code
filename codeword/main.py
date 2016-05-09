from lib.w2v.w2v import *

import logging
import os.path
import sys

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))

# build sentences
# newsgroup_sentences = build_sentences("./data/newsgroup")
# enron_sentences = build_sentences("./data/enron")
# wiki_sentences = build_sentences("./data/wiki")

# train models
# newsgroup_model = model_from_sentences(newsgroup_sentences)
# newsgroup_model.save_word2vec_format("./temp/models/newsgroup", binary=False)
#
# enron_model = model_from_sentences(enron_sentences)
# enron_model.save_word2vec_format("./temp/models/enron", binary=False)

# wiki_model = model_from_sentences(wiki_sentences)
# wiki_model.save_word2vec_format("./temp/models/wiki", binary=False)

# load models
newsgroup_model = model_from_saved("./temp/models-external/google.bin", binary=True)
enron_model = model_from_saved("./temp/models-clic/enron", binary=False)

intersect_vocab = intersect_vocab(enron_model, newsgroup_model)
vocabs = {}

from scipy import spatial

for word in intersect_vocab:
    cosine_sim = 1 - spatial.distance.cosine(newsgroup_model[word], enron_model[word])
    vocabs[word] = cosine_sim

from scipy.stats import norm

mu, std = norm.fit(vocabs.values())

print mu
print std
print vocabs['meeting']
print vocabs['raptor']

tolerance = 0.005
for word in vocabs.keys():
    p = norm.cdf(vocabs[word], mu, std)
    if (p < tolerance) or (p > 1 - tolerance):
        print ("%f %s" % (vocabs[word], word))

import matplotlib.pyplot as plot

plot.hist(vocabs.values(), bins=100)
plot.show()