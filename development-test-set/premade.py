
import cPickle as pickle

import logging, os, sys

logger = logging.getLogger('root')

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))

wsj_substitute_key = pickle.load(open('substitute_keys/wsj_substitute_key.pkl', 'rb'))

import lib.model_loaders.codeword_model_loader as codeword_model_loader

wsj = codeword_model_loader.CodewordModel('./models/wsj_substituted_w2v.mdl')

import lib.model_loaders.wiki_model_loader as wiki_model_loader

wiki = wiki_model_loader.WikiModelLoader('./models/wiki_original/en.model')

import lib.model_loaders.google_model_loader as google_model_loader

google = google_model_loader.GoogleModelLoader('./models/googlenews_original.bin')

print wsj.get_similar_words('finance')

print wiki.get_similar_words('finance')

print google.get_similar_words('finance')

vocabs = {}
i = 0

for word in wsj.model.vocab:
    if word in google.model.vocab and word in wiki.model.vocab:
        if i % 100 is 0:
            logger.info('%d: %s' % (i, word))
            pickle.dump(vocabs, open('vocabs_reference_%d.pkl' % i, 'wb'))
        wsj_set = set([a[0] for a in wsj.get_similar_words(word)])    
        google_set = set([a[0] for a in google.get_similar_words(word)])
        wiki_set = set([a[0] for a in wiki.get_similar_words(word)])
    
        google_count = len(wsj_set & google_set)
        wiki_count = len(wsj_set & wiki_set)
        
        vocabs[word] = {'google_count': google_count, 'wiki_count': wiki_count}
    i += 1

logger.info('Completely iterated')

pickle.dump(vocabs, open('vocabs_reference.pkl', 'wb'))

vocabs_loaded = pickle.load(open('vocabs_reference.pkl', 'r'))
