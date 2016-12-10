#!/usr/bin/env python
# encoding=utf-8
# coding=utf-8
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

coding = 'utf-8'
import sys

reload(sys)
sys.setdefaultencoding(coding)
import Tools
import jieba.posseg as pseg
import pandas as pd

category_dic = {'产品': 1, '服务': 2, '平台': 3, '其他': 4, '业务': 5}
sentiment_dic = {'好评': 3, '中评': 2, '差评': 1}

import csv
import codecs
import numpy as np
import load_google_w2v_bin_file
def get_vector_for_sentence(sentence):
    cut_result = Tools.get_cut_result_for_sentence_with_no_stop_word_or_number(sentence)
    vec = np.arange(200)
    for word in cut_result:
        vec = vec + load_google_w2v_bin_file.get_vec_for_word(str(word).encoding('utf8'))
    return vec / len(cut_result)

def get_X_train():
    dir = '../data/labeledreview.xlsx'
    x_train = Tools.get_sentences_from_excel(dir, [0, 1, 2, 3, 4])
    x_train_transfered = []
    for line in x_train:
        comment = line[1].encode('utf8')
        line_index = str(line[0]).encode('utf8')
        dimension = line[3].encode('utf8')
        sentiment_label = line[4].encode('utf8')
        sentence_vec = get_vector_for_sentence(comment)

        x_train.append([sentence_vec, ])
        print '?'
    return


def get_Y_train():
    return


get_X_train()
