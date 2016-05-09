__author__ = 'linanqiu'

import gensim


class WikiModelLoader:
    def __init__(self, filename):
        self.model = gensim.models.Word2Vec.load(filename)

    def get_similar_words(self, word, count=500):
        return self.model.most_similar(word, topn=count)
