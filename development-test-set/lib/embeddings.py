__author__ = 'linanqiu'

import glob
import cPickle as pickle
import logging
import os
import sys

logger = logging.getLogger('embeddings')

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))

import sentences


def embeddings_wsj():
    import gensim

    logger.info('Loading sentences')
    sents = sentences.Sentences(dirname='../data/', prefix='wsj_corpus')

    logger.info('Generating embeddings')
    model = gensim.models.Word2Vec(sents, min_count=5, workers=8, iter=100, window=15, size=300, negative=25)

    logger.info('Saving model')
    model.save_word2vec_format('./models/wsj-original-w2v.mdl', binary=True)


embeddings_wsj()
