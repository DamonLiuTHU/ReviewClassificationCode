#!/usr/bin/env python
# -*- coding: utf-8 -*-

coding = 'latin-1'
import sys

reload(sys)
sys.setdefaultencoding(coding)

from gensim.models import Word2Vec as wv

model = wv.load_word2vec_format('./vectors_new_binary.bin', binary=True, encoding=coding)

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def get_vec_for_word(word):
    return model[word]

    # a_word_vec = get_vec_for_word('京东')
    # print a_word_vec.shape

