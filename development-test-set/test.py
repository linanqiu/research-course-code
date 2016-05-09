__author__ = 'linanqiu'

import cPickle as pickle

import logging, os, sys

logger = logging.getLogger('root')

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))

import lib.model_loaders.codeword_model_loader as codeword_model_loader

wsj = codeword_model_loader.CodewordModel('./models/wsj_substituted_w2v.mdl')
print wsj.get_similar_words('credit')

import lib.model_loaders.wiki_model_loader as wiki_model_loader

wiki = wiki_model_loader.WikiModelLoader('./models/wiki_original/en.model')
print wiki.get_similar_words('credit')
print wiki.get_similar_words('finance')