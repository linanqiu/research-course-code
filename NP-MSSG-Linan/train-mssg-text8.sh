#!/bin/sh

classpath=`cat CP.hack`
wordvec_app="java -Xmx10g -cp ${classpath} WordVec"

${wordvec_app} --model=MSSG-MaxOut --train=data/text8_replaced --output=data/text8-vectors-MSSG.gz --sense=2 --learn-top-v=4000 --size=300 --window=5 --min-count=15  --threads=15  --negative=1 --sample=0.001 --binary=1 --ignore-stopwords=1 --encoding=ISO-8859-15 --save-vocab=data/text8_replaced.vocab.gz --rate=0.025 --delta=0.1
