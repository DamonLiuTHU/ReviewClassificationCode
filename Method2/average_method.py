#!/usr/bin/env python
# -*- coding: utf-8 -*-

coding = 'utf-8'
import sys

reload(sys)
sys.setdefaultencoding(coding)


def get_sentence_vector(sentence):
    return []


def get_X_train():
    x_train = []
    file = open('../txtfiles/chanpin.txt')
    rows = file.readlines()
    for line in rows:
        sentence_vector = get_sentence_vector(line)
        x_train.append(sentence_vector)
    return x_train


def get_Y_train():
    return
