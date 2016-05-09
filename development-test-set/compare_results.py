from __future__ import division

__author__ = 'linanqiu'

from w2v.w2v import *

import logging
import os.path
import sys
from itertools import izip
import cPickle as pickle

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))

vocabs = pickle.load(open('vocabs-compared.pkl', 'rb'))

codewords = sorted(vocabs, key=vocabs.get)

substitute_key = pickle.load(open('substitute-key.pkl', 'rb'))

positive = 0
false_positive = 0
count = 1
results = {}

for word in codewords:
    if word in substitute_key:
        positive += 1
    else:
        false_positive += 1
    results[count] = {'count': count, 'positive': positive, 'false_positive': false_positive, 'false_negative': len(substitute_key) - positive}
    count += 1

import pandas as pd
import matplotlib
import matplotlib.pyplot as plot
matplotlib.style.use('ggplot')

# distribution of comparison counts
plot.hist(vocabs.values(), bins=100)
plot.show()

# plot results
dataframe = pd.DataFrame.from_dict(results, orient='index')
print(dataframe)

dataframe.plot(x='count', y=['positive', 'false_positive', 'false_negative'], xlim=[0, 200], ylim=[0, 100])
plot.show()