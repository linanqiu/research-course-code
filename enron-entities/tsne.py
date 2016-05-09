from sklearn.manifold import TSNE
import gzip
import cPickle as pickle

embeddings_np = pickle.load(gzip.open('embeddings_np.pklz', 'rb'))
model_2d = TSNE()
embeddings_2d = model_2d.fit_transform(embeddings_np)
pickle.dump(embeddings_2d, gzip.open('embeddings_2d.pklz', 'wb'))
