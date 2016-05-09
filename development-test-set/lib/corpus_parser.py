__author__ = 'linanqiu'

import logging
import os.path
import sys
import cPickle as pickle

logger = logging.getLogger('corpus_parser')

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))


# returns lists of sentence, each sentence is a list of words, lower case.
def parse_wsj():
    import nltk.corpus as corpus

    logger.info('Parsing WSJ Corpus')

    corpus_root = "../data/LDC99T42-Treebank-3/package/treebank_3/parsed/mrg/wsj"
    file_pattern = ".*/wsj_.*\.mrg"

    reader = corpus.BracketParseCorpusReader(corpus_root, file_pattern)

    count = 1

    sents = []
    for fileid in reader.fileids():
        sent_lower = [word.lower() for word in reader.words(fileids=fileid)]
        sents.append(sent_lower)
        if (count % 5000 == 0):
            pickle.dump(sents, open('../data/wsj_corpus_%d.pkl' % count, 'wb'))
            sents = []
        count += 1
    pickle.dump(sents, open('../data/wsj_corpus_%d.pkl' % count, 'wb'))


def parse_nyt():
    import glob
    import nltk.corpus as corpus

    logger.info('Parsing NYT Corpus')

    tars = glob.glob('../data/LDC2008T19-New-York-Times-Annotated/data/*/*.tgz')

    import tarfile

    logger.info('Extracting tars')
    for tar in tars:
        logger.info('Extracting %s' % tar)
        tar_file = tarfile.open(tar, 'r')

        extract_path = os.path.dirname(os.path.realpath(tar))

        if not os.path.exists(os.path.realpath(tar.replace('.tgz', ''))):
            tar_file.extractall(extract_path)

    logger.info('Getting XML paths')
    xmls = glob.glob(
        '../data/LDC2008T19-New-York-Times-Annotated/data/*/*/*/*.xml')

    xml_paths = [os.path.realpath(xml) for xml in xmls]

    reader = corpus.XMLCorpusReader('', xml_paths)

    sents = []
    count = 1
    for fileid in xml_paths:
        logger.info('Normalizing %s' % fileid)
        sent_lower = [word.lower() for word in reader.words(fileid=fileid)]
        sents.append(sent_lower)

        if (count % 5000 == 0):
            pickle.dump(sents, open('../data/nyt_corpus_%d.pkl' % count, 'wb'))
            sents = []
        count += 1
    pickle.dump(sents, open('../data/nyt_corpus_%d.pkl' % count, 'wb'))


def parse_wiki():
    import glob
    finished_pickles = glob.glob('../data/wiki_corpus_*.pkl')
    line_counts = [int(finished_pickle.replace('../data/wiki_corpus_', '').replace('.pkl', '')) for finished_pickle in
                   finished_pickles]
    max_line = max(line_counts)

    import nltk

    sents = []
    count = 1
    with open('../data/English-Wikipedia-Snapshot-04-08-10/wiki-plaintext-clean', 'r') as wiki_file:
        for line in wiki_file:
            if count < max_line:
                count += 1
                continue

            try:
                sent_lower = [word.lower() for word in nltk.word_tokenize(line)]
            except UnicodeDecodeError:
                logger.info('UnicodeDecodeError. Ignoring line %d' % count)

            if len(sent_lower) > 0:
                sents.append(sent_lower)
            if (count % 50000 == 0):
                logger.info('Normalizing line %d' % count)
                pickle.dump(sents, open('../data/wiki_corpus_%d.pkl' % count, 'wb'))
                sents = []
            count += 1
        pickle.dump(sents, open('../data/wiki_corpus_%d.pkl' % count, 'wb'))


def parse_reddit():
    import sentences
    import csv

    comments_file = '../data/reddit/comments.csv'
    threads_file = '../data/reddit/threads.csv'

    data = {}

    def process_text(text):
        return pattern.sub('', text)

    def process_row(subreddit, metareddit, row):

        key = '%s_%s' % (metareddit, subreddit)
        row[0] = process_text(row[0])

        if key in data:
            data[key].append(row)
        else:
            data[key] = []
            data[key].append(row)

    import re, string
    pattern = re.compile('[^\s\w]+')

    with open(comments_file, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            process_row(row[2], row[3], row)

    with open(threads_file, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            process_row(row[4], row[5], row)

    for key, value in data.iteritems():
        logger.info('Writing %s' % key)
        with open('../data/reddit_divided/%s.csv' % key, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerows(value)


parse_reddit()

# logger.info('Begin Parsing NYT')
# parse_nyt()
#
# logger.info('Begin Parsing Wiki')
# parse_wiki()
