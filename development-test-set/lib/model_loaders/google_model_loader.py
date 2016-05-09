__author__ = 'linanqiu'

import gensim


class GoogleModelLoader:
    def __init__(self, filename):
        self.model = gensim.models.Word2Vec.load_word2vec_format(filename, binary=True)

    def get_similar_words(self, word, count=500):
        return self.model.most_similar(word, topn=count)
