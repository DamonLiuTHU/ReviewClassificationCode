import jieba.posseg as jieba
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
utf8 = 'utf8'


def is_stop_word(word):
    stopwordslist = [line.strip().decode('utf-8') for line in open('../txtfiles/stopword.txt').readlines()]
    return word in stopwordslist


import re


def is_number(word):
    result = re.match('\d+', word)
    return result


def read_content_from_txt_with_paths(paths):
    # contents = []
    target = '../txtfiles/split.txt'
    target = open(target, 'w')
    for path in paths:
        file = open(path, 'r')
        rows = file.readlines()
        for row in rows:
            split_result = jieba.cut(row)
            for w in split_result:
                if is_stop_word(w.word) or w.flag == 'x' or w.flag == 'eng' or is_number(w.word):
                    continue
                else:
                    # contents.append(w.word)
                    target.write(w.word + ' ')
    target.close()
    return


def get_cut_result_for_sentence_with_no_stop_word_or_number(sentence):
    result = []
    split_result = jieba.cut(sentence)
    for w in split_result:
        if is_stop_word(w.word) or w.flag == 'x' or w.flag == 'eng' or is_number(w.word):
            continue
        else:
            # contents.append(w.word)
            result.append(w.word)
    return result


import xlrd


def get_sentences_from_excel(path, column_index_list):
    result = []
    xlrd.Book.encoding = utf8
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    nrows = table.nrows
    print 'count rows in path :' + str(nrows), path
    for i in range(nrows):
        comment = []
        for index in column_index_list:
            comment.append((table.row_values(i)[index:index + 1])[0])
        result.append(comment)
    return result

# paths = ['../txtfiles/chanpin.txt',
#          '../txtfiles/fuwu.txt', '../txtfiles/pingtai.txt', '../txtfiles/qita.txt',
#          '../txtfiles/yewu.txt', '../txtfiles/reviews.txt']
# read_content_from_txt_with_paths(paths)
