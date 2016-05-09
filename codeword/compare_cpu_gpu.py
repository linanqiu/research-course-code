from lib.w2v.w2v import *

# logging
import logging
import os.path
import sys

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))

# load models
cpu_model = model_from_saved("./temp/models-ec2/enron", binary=False)
gpu_model = model_from_saved("./temp/models-gpu/enron", binary=False)

from scipy import spatial

vocabs = {}

for word in cpu_model.vocab:
    if word in cpu_model and word in gpu_model:
        cosine_sim = 1 - spatial.distance.cosine(cpu_model[word], gpu_model[word])
        vocabs[word] = cosine_sim

import matplotlib.pyplot as plot

plot.hist(vocabs.values(), bins=100)
plot.show()

