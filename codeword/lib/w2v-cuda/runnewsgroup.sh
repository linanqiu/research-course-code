#!/usr/bin/env bash
./word2vec -train ../../data/newsgroup/20NewsGroup.clean -output ../../temp/models-gpu/newsgroup -cbow 1 -size 300 -window 15 -negative 25 -hs 0 -sample 1e-4 -binary 0 -iter 300 -min-count 5
