#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from gensim_test.models import Word2Vec
# 主程序
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = Word2Vec.Text8Corpus(u"../split.txt")  # load input files
model = Word2Vec.Word2Vec(sentences, size=200)  # 训练skip-gram模型; 默认window=5

# 计算两个词的相似度/相关程度
y1 = model.similarity(u"不错", u"好")
print u"【不错】和【好】的相似度为：", y1
print "--------\n"

# 计算某个词的相关词列表
y2 = model.most_similar(u"书", topn=20)  # 20个最相关的
print u"和【书】最相关的词有：\n"
for item in y2:
    print item[0], item[1]
print "--------\n"

# 寻找对应关系
print u"书-不错，质量-"
y3 = model.most_similar([u'质量', u'不错'], [u'书'], topn=3)
for item in y3:
    print item[0], item[1]
print "--------\n"

# 寻找不合群的词
y4 = model.doesnt_match(u"书 书籍 教材 很".split())
print u"不合群的词：", y4
print "--------\n"

# 保存模型，以便重用
model.save(u"review.model")
# 对应的加载方式
# model_2 = word2vec.Word2Vec.load("text8.model")

# 以一种C语言可以解析的形式存储词向量
model.save_word2vec_format(u"review.model.bin", binary=True)
# 对应的加载方式
# model_3 = word2vec.Word2Vec.load_word2vec_format("text8.model.bin", binary=True)

if __name__ == "__main__":
    pass