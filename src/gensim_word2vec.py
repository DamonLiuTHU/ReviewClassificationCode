#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gensim, logging
# import modules & set up logging
import gensim, logging

utf8 = 'utf8'
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# sentences = [['first', 'sentence'], ['second', 'sentence']]
# train word2vec on the two sentences
# model = gensim.models.Word2Vec(sentences, min_count=1)
import xlrd
import Tools


def get_sentence_list():
    import jieba.posseg as pseg
    sentence_list = []

    tmp = Tools.get_sentences_from_excel('../data/彩电业务.xlsx', [3, 4])
    counter = len(tmp)
    for line in tmp:
        counter -= 1
        print 'left:', counter,' total:',len(tmp)
        sentence = []
        if len(line) == 0:
            continue
        comment = line[0]
        if type(comment) != unicode:
            continue
        str_c = comment.encode(utf8)
        if str_c == 'sentence':
            continue
        seg_list = pseg.cut(str_c)
        for w in seg_list:
            if w.flag != 'x' and w.flag != 'eng':
                sentence.append(w.word)
        # model.train(line)
        sentence_list.append(sentence)

    tmp = Tools.get_sentences_from_excel('../data/彩电产品.xlsx', [3, 4])
    counter = len(tmp)
    for line in tmp:
        counter -= 1
        print 'left:', counter, ' total:', len(tmp)
        sentence = []
        if len(line) == 0:
            continue
        comment = line[0]
        if type(comment) != unicode:
            continue
        str_c = comment.encode(utf8)
        seg_list = pseg.cut(str_c)
        for w in seg_list:
            if w.flag != 'x' and w.flag != 'eng':
                sentence.append(w.word)
        # model.train(line)
        sentence_list.append(sentence)
    tmp = Tools.get_sentences_from_excel('../data/彩电平台.xlsx', [3, 4])
    counter = len(tmp)
    for line in tmp:
        counter -= 1
        print 'left:', counter, ' total:', len(tmp)
        sentence = []
        if len(line) == 0:
            continue
        comment = line[0]
        if type(comment) != unicode:
            continue
        str_c = comment.encode(utf8)
        seg_list = pseg.cut(str_c)
        for w in seg_list:
            if w.flag != 'x' and w.flag != 'eng':
                sentence.append(w.word)
        # model.train(line)
        sentence_list.append(sentence)


    tmp = Tools.get_sentences_from_excel('../data/彩电服务.xlsx', [3, 4])
    counter = len(tmp)
    for line in tmp:
        counter -= 1
        print 'left:', counter, ' total:', len(tmp)
        sentence = []
        if len(line) == 0:
            continue
        comment = line[0]
        if type(comment) != unicode:
            continue
        str_c = comment.encode(utf8)
        seg_list = pseg.cut(str_c)
        for w in seg_list:
            if w.flag != 'x' and w.flag != 'eng':
                sentence.append(w.word)
        # model.train(line)
        sentence_list.append(sentence)

    tmp = Tools.get_sentences_from_excel('../data/彩电其他.xlsx', [1, 2])
    counter = len(tmp)
    for line in tmp:
        counter -= 1
        print 'left:', counter, ' total:', len(tmp)
        sentence = []
        if len(line) == 0:
            continue
        comment = line[0]
        if type(comment) != unicode:
            continue
        str_c = comment.encode(utf8)
        seg_list = pseg.cut(str_c)
        for w in seg_list:
            if w.flag != 'x' and w.flag != 'eng':
                sentence.append(w.word)
        # model.train(line)
        sentence_list.append(sentence)

    path = '../data/comment_origin.xlsx'
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    nrows = table.nrows

    print 'count rows in path :' + str(nrows)

    for i in range(1, nrows):
        # print 'left:', nrows-i, ' total:', nrows
        line = []
        comment = table.row_values(i)[1:1 + 1][0]
        if type(comment) != unicode:
            continue
        str_c = comment.encode(utf8)
        seg_list = pseg.cut(str_c)
        for w in seg_list:
            if w.flag != 'x' and w.flag != 'eng':
                line.append(w.word)
        # model.train(line)
        sentence_list.append(line)

    return sentence_list


# model = gensim.models.Word2Vec(get_sentence_list(), min_count=1)
# model.save(u"review.model.bin")


model = gensim.models.Word2Vec.load(u"review.model.bin")


# # 计算两个词的相似度/相关程度
# y1 = model.similarity(u"不错", u"好")
# print u"【不错】和【好】的相似度为：", y1
# print "--------\n"
#
# # 计算某个词的相关词列表
# y2 = model.most_similar(u"京东", topn=20)  # 20个最相关的
# print u"和【书】最相关的词有：\n"
# for item in y2:
#     print item[0], item[1]
# print "--------\n"
#
# # 寻找对应关系
# print u"书-不错，质量-"
# y3 = model.most_similar([u'质量', u'不错'], topn=3)
# for item in y3:
#     print item[0], item[1]
# print "--------\n"
#
# y4 = model[u'京东']
# print y4, type(y4), y4.shape


def get_vector_for_unicode_word(word):
    return model[word]
