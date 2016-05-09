__author__ = 'linanqiu'

from lib.w2v.w2v import *

import logging
import os.path
import sys

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))

from itertools import izip

enron_model = model_from_saved("./temp/models-clic/enron", binary=False)
reference_model = model_from_saved("./temp/models-external/google.bin", binary=True)