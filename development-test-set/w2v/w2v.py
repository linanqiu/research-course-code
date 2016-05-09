__author__ = 'linanqiu'

def build_sentences(all_lines_filename):

    import cPickle as pickle

    class Sentence(object):
        def __init__(self, all_lines_filename):
            self.all_lines = pickle.load(open(all_lines_filename, 'rb'))

        def __iter__(self):
            for line in self.all_lines:
                yield line

    sentences = Sentence(all_lines_filename)
    return sentences

def model_from_sentences(sentences):
    import gensim

    model = gensim.models.Word2Vec(sentences, min_count=5, workers=8, iter=300, window=15, size=300, negative=25)

    return model

def model_from_saved(filename, binary):
    import gensim

    model = gensim.models.Word2Vec.load_word2vec_format(filename, binary=binary)
    return model

def model_from_external(filename, binary):
    import gensim

    model = gensim.models.Word2Vec.load(filename, binary=binary)
    return model

def intersect_vocab(model1, model2):
    intersect_vocab = set(model1.vocab).intersection(set(model2.vocab))
    return intersect_vocab