def build_sentences(datadir):

    import os

    class Sentence(object):
        def __init__(self, dirname):
            self.dirname = dirname

        def __iter__(self):
            for fname in os.listdir(self.dirname):
                for line in open (os.path.join(self.dirname, fname)):
                    yield line.split()

    sentences = Sentence(datadir)
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
