#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gensim, logging
# import modules & set up logging
import gensim, logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = [['first', 'sentence'], ['second', 'sentence']]
# train word2vec on the two sentences
model = gensim.models.Word2Vec(sentences, min_count=1)
import xlrd


def get_sentence_list():
    path = '../data/comment_origin.xlsx'
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    nrows = table.nrows
    utf8 = 'utf8'
    print 'count rows in path :' + str(nrows)
    import jieba.posseg as pseg
    sentence_list = []
    for i in range(1, nrows):
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


# model = gensim.models.Word2Vec(get_sentence_list, min_count=1)
# model.save(u"review.model.bin", binary=True)
model = gensim.models.Word2Vec.load_word2vec_format(u"review.model.bin",binary=True)
# 计算两个词的相似度/相关程度
y1 = model.similarity(u"不错", u"好")
print u"【不错】和【好】的相似度为：", y1
print "--------\n"

# 计算某个词的相关词列表
y2 = model.most_similar(u"京东", topn=20)  # 20个最相关的
print u"和【书】最相关的词有：\n"
for item in y2:
    print item[0], item[1]
print "--------\n"

# 寻找对应关系
print u"书-不错，质量-"
y3 = model.most_similar([u'质量', u'不错'], topn=3)
for item in y3:
    print item[0], item[1]
print "--------\n"
