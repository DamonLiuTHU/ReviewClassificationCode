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

import csv
import codecs
import numpy as np
import load_google_w2v_bin_file
import gensim_word2vec

category_dic = {'产品': np.array([1, 0, 0, 0, 0]),
                '服务': np.array([0, 1, 0, 0, 0]),
                '平台': np.array([0, 0, 1, 0, 0]),
                '其他': np.array([0, 0, 0, 1, 0]),
                '业务': np.array([0, 0, 0, 0, 1])}
sentiment_dic = {'好评': 3, '中评': 2, '差评': 1, '其他': -1}


def get_vector_for_sentence(sentence):
    cut_result = Tools.get_cut_result_for_sentence_with_no_stop_word_or_number(sentence)
    vec = np.zeros(100, dtype=np.int)
    for word in cut_result:
        vec = vec + gensim_word2vec.get_vector_for_unicode_word(word)
    return vec / len(cut_result)


def get_X_train():
    dir = '../data/labeledreview.xlsx'
    x_train = Tools.get_sentences_from_excel(dir, [0, 1, 2, 3, 4])
    x_train_transfered = []
    y_train = []
    counter = 0
    for line in x_train:
        counter += 1
        print counter, '/', len(x_train)
        comment = line[1]
        line_index = str(line[0])
        dimension = line[3].encode('utf8')
        sentiment_label = line[4].encode('utf8')
        sentence_vec = get_vector_for_sentence(comment)
        label = category_dic[dimension] * sentiment_dic[sentiment_label]
        x_train_transfered.append(sentence_vec)
        y_train.append(label)
        # print sentence_vec
        # print label
    return x_train_transfered, y_train


x_train, y_train = get_X_train()
from sklearn import svm, cross_validation

# model = svm.SVC()
# model.fit
clf = svm.SVC(kernel='linear', C=1)
scores = cross_validation.cross_val_score(clf, x_train, y_train, cv=5, score_func=None)
print scores
