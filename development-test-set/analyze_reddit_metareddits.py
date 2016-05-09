import logging
import os
import sys

logger = logging.getLogger('root')

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))

import cPickle as pickle

import numpy


def analyze_metareddit(metareddit):
  reddit_substitute_key = pickle.load(
      open('substitute_keys/reddit_%s_substitute_key.pkl' % metareddit, 'rb'))

  import lib.model_loaders.codeword_model_loader as codeword_model_loader

  reddit_substituted = codeword_model_loader.CodewordModel(
      './models/reddit_%s_substituted_w2v.mdl' % metareddit)

  import lib.model_loaders.wiki_model_loader as wiki_model_loader

  reddit_original = codeword_model_loader.CodewordModel(
      './models/reddit_original_w2v.mdl')

  vocabs = {}
  i = 0

  for word in reddit_substituted.model.vocab:
    if word in reddit_original.model.vocab:
      if i % 1000 is 0:
        logger.info('%d: %s' % (i, word))
      reddit_substituted_set = set(
          [a[0] for a in reddit_substituted.get_similar_words(word)])
      reddit_original_set = set(
          [a[0] for a in reddit_original.get_similar_words(word)])

      count = len(reddit_substituted_set & reddit_original_set)

      vocabs[word] = {'count': count}
    i += 1

  pickle.dump(vocabs, open(
      'reddit_vocabs_reference/vocabs_reference_reddit_%s.pkl' % metareddit, 'wb'))


def analyze_all():
  reddit_substitute_key = pickle.load(
      open('substitute_keys/reddit_substitute_key.pkl', 'rb'))

  import lib.model_loaders.codeword_model_loader as codeword_model_loader

  reddit_substituted = codeword_model_loader.CodewordModel(
      './models/reddit_substituted_w2v.mdl')

  import lib.model_loaders.wiki_model_loader as wiki_model_loader

  reddit_original = codeword_model_loader.CodewordModel(
      './models/reddit_original_w2v.mdl')

  vocabs = {}
  i = 0

  for word in reddit_substituted.model.vocab:
    if word in reddit_original.model.vocab:
      if i % 1000 is 0:
        logger.info('%d: %s' % (i, word))
      reddit_substituted_set = set(
          [a[0] for a in reddit_substituted.get_similar_words(word)])
      reddit_original_set = set(
          [a[0] for a in reddit_original.get_similar_words(word)])

      count = len(reddit_substituted_set & reddit_original_set)

      vocabs[word] = {'count': count}
    i += 1

  pickle.dump(vocabs, open(
      'reddit_vocabs_reference/vocabs_reference_reddit.pkl', 'wb'))


def main():
  analyze_all()

  metareddits = ['entertainment', 'gaming', 'humor',
                 'learning', 'lifestyle', 'news', 'television']
  for metareddit in metareddits:
    analyze_metareddit(metareddit)

main()
