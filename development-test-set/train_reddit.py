__author__ = 'linanqiu'

import lib.sentences as sentences
import gensim
import logging, os, sys
import cPickle as pickle

import lib.substitute as substitute

logger = logging.getLogger('root')

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))

communities = ['entertainment', 'gaming', 'humor', 'learning', 'lifestyle', 'news', 'television']
import glob

# logger.info('Generating substitute key for entire corpus')
# all_files = glob.glob('./data/reddit_divided/*.csv')
# reddit_substitute_key_all, reddit_substitute_key_sorted_tfidf_all = substitute.generate_substitute_key_reddit(100, all_files)
# substitute.write_substitute_key(reddit_substitute_key_all, reddit_substitute_key_sorted_tfidf_all, 'reddit_substitute_key')

# for community in communities:
#     logger.info('Generating substitute key for %s' % community)
#     files = glob.glob('./data/reddit_divided/%s_*.csv' % community)
#
#     reddit_substitute_key, reddit_substitute_key_sorted_tfidf = substitute.generate_substitute_key_reddit(100, files)
#     substitute.write_substitute_key(reddit_substitute_key, reddit_substitute_key_sorted_tfidf,
#                                     'reddit_%s_substitute_key' % community)

logger.info('Generating embeddings for entire original corpus')
all_files = glob.glob('./data/reddit_divided/*.csv')
sents = sentences.OmegaRedSentences(all_files, substitute=None, substitute_key=None)
model = gensim.models.Word2Vec(sents, min_count=5, workers=8, iter=100, window=15, size=300, negative=25)
model.save_word2vec_format('./models/reddit_original_w2v.mdl', binary=True)

# logger.info('Generating embeddings for entire substituted corpus')
# all_files = glob.glob('./data/reddit_divided/*.csv')
# reddit_substitute_key_all = pickle.load(open('./substitute_keys/reddit_substitute_key.pkl', 'r'))
# sents = sentences.OmegaRedSentences(all_files, substitute='_', substitute_key=reddit_substitute_key_all)
# model = gensim.models.Word2Vec(sents, min_count=5, workers=8, iter=100, window=15, size=300, negative=25)
# model.save_word2vec_format('./models/reddit_substituted_w2v.mdl', binary=True)

# for community in communities:
#     logger.info('Generating embeddings for %s' % community)
#     files = glob.glob('./data/reddit_divided/*.csv')
#
#     substitute_key = pickle.load(open('./substitute_keys/reddit_%s_substitute_key.pkl' % community, 'r'))
#     sents = sentences.OmegaRedSentences(files, substitute='%s_' % community, substitute_key=substitute_key)
#     model = gensim.models.Word2Vec(sents, min_count=5, workers=8, iter=100, window=15, size=300, negative=25)
#     model.save_word2vec_format('./models/reddit_%s_substituted_w2v.mdl' % community, binary=True)

# for community in communities:
#     logger.info('Generating embeddings for only substituted portion of %s' % community)
#     files = glob.glob('./data/reddit_divided/%s_*.csv' % community)

#     substitute_key = pickle.load(open('./substitute_keys/reddit_%s_substitute_key.pkl' % community, 'r'))
#     sents = sentences.OmegaRedSentences(files, substitute='%s_' % community, substitute_key=substitute_key)
#     model = gensim.models.Word2Vec(sents, min_count=5, workers=8, iter=100, window=15, size=300, negative=25)
#     model.save_word2vec_format('./models/reddit_%s_substituted_community_only_w2v.mdl' % community, binary=True)

# communities.reverse()

# for community in communities:
#     logger.info('Generating embeddings for only substituted portion of %s' % community)
#     files = glob.glob('./data/reddit_divided/%s_*.csv' % community)

#     substitute_key = pickle.load(open('./substitute_keys/reddit_%s_substitute_key.pkl' % community, 'r'))
#     sents = sentences.OmegaRedSentences(files, substitute=None, substitute_key=None)
#     model = gensim.models.Word2Vec(sents, min_count=5, workers=8, iter=100, window=15, size=300, negative=25)
#     model.save_word2vec_format('./models/reddit_%s_original_community_only_w2v.mdl' % community, binary=True)
