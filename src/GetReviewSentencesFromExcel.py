# _*_ coding: utf-8 _*_
# coding=utf-8
import xlrd
import jieba.posseg as pseg
import sys
import xlsxwriter

reload(sys)
sys.setdefaultencoding('utf-8')
utf8 = 'utf8'


def get_sentences_from_excel(path, txtName, columnIndex):
    review_list_file = open('../txtfiles/' + txtName + '.txt', 'w')
    split_word_result = open('../split.txt', 'w')
    xlrd.Book.encoding = utf8
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    nrows = table.nrows
    print 'count rows in path :' + str(nrows)
    for i in range(1, nrows):
        comment = table.row_values(i)[columnIndex:columnIndex + 1]
        str_c = str(comment[0])
        str_c = str_c.encode(utf8)
        review_list_file.write(str_c + '\n')
        seg_list = pseg.cut(str_c)
        for w in seg_list:
            if w.flag != 'x' and w.flag != 'eng':
                split_word_result.write(w.word + ' ')
        print w.word, w.flag
    review_list_file.close()
    split_word_result.close()
    return


def get_sentences_from_excel(path, columnIndex):
    result = []
    split_word_result = open('../split.txt', 'w')
    xlrd.Book.encoding = utf8
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    nrows = table.nrows
    print 'count rows in path :' + str(nrows)
    for i in range(1, nrows):
        comment = table.row_values(i)[columnIndex:columnIndex + 1]
        str_c = str(comment[0])
        str_c = str_c.encode(utf8)
        result.append(str_c)
        seg_list = pseg.cut(str_c)
        for w in seg_list:
            if w.flag != 'x' and w.flag != 'eng':
                split_word_result.write(w.word + ' ')
        print w.word, w.flag
    split_word_result.close()
    return result


def get_sentences_from_excel(path, column_index_list):
    result = []
    xlrd.Book.encoding = utf8
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    nrows = table.nrows
    print 'count rows in path :' + str(nrows)
    for i in range(1, nrows):
        comment = []
        for index in column_index_list:
            comment.append(table.row_values(i)[index:index + 1][0])
        result.append(comment)
    return result


import re


def is_number(word):
    result = re.match('\d+', word)
    return result


def getSegment(sentence, stopwordslist):
    seg_list = pseg.cut(sentence)  # 分词
    result = ''
    for w in seg_list:
        if is_stop_word(w.word) or w.flag == 'x' or w.flag == 'eng' or is_number(w.word):
            continue
    else:
        # contents.append(w.word)
        result += (w.word + ' ')
    return result


def getRowsFromFile(path):
    file = open(path)
    rows = file.readlines()
    return rows


def is_stop_word(word):
    stopwordslist = [line.strip().decode('utf-8') for line in open('../txtfiles/stopword.txt').readlines()]
    return word in stopwordslist


def form_a_xls_with_every_reviews():
    review_set = set()  # 创建空的集合
    xls = xlsxwriter.Workbook('../labeledreview.xlsx')  # 创建一个excel文件
    xls.encoding = utf8  # 设置编码为utf-8
    sheet1 = xls.add_worksheet('default')  # 创建一个工作表对象
    filename = '../txtfiles/chanpin.txt'
    file = open(filename)
    rows = file.readlines()  # 自动将文本划分成一个行的列表
    row_index = 0

    # stopwordslist = {}.fromkeys([ line.rstrip() for line in open('../txtfiles/stopword.txt') ])      #读取停用词
    stopwordslist = [line.strip().decode('utf-8') for line in open('../txtfiles/stopword.txt').readlines()]

    for sentence in rows:
        if review_set.__contains__(sentence):  # 查看sentence是不是在集合内，是的话忽略
            continue
        review_set.add(sentence)
        sheet1.write(row_index, 0, row_index)
        sentence = sentence.rstrip('\n').encode(utf8)
        sheet1.write(row_index, 1, sentence)
        seg_result = getSegment(sentence, stopwordslist)  # 分词
        seg_result = seg_result.encode(utf8)
        sheet1.write(row_index, 2, seg_result)
        label = '产品'.encode(utf8)
        label_index = 0
        sheet1.write(row_index, 3, label)
        sheet1.write(row_index, 4, label_index)
        row_index += 1

    rows = getRowsFromFile('../txtfiles/fuwu.txt')
    for sentence in rows:
        if review_set.__contains__(sentence):
            continue
        review_set.add(sentence)
        sheet1.write(row_index, 0, row_index)
        sentence = sentence.rstrip('\n').encode(utf8)
        sheet1.write(row_index, 1, sentence)
        seg_result = getSegment(sentence, stopwordslist)
        seg_result = seg_result.encode(utf8)
        sheet1.write(row_index, 2, seg_result)
        label = '服务'.encode(utf8)
        label_index = 1
        sheet1.write(row_index, 3, label)
        sheet1.write(row_index, 4, label_index)
        row_index += 1

    rows = getRowsFromFile('../txtfiles/pingtai.txt')
    for sentence in rows:
        if review_set.__contains__(sentence):
            continue
        review_set.add(sentence)
        sheet1.write(row_index, 0, row_index)
        sentence = sentence.rstrip('\n').encode(utf8)
        sheet1.write(row_index, 1, sentence)
        seg_result = getSegment(sentence, stopwordslist)
        seg_result = seg_result.encode(utf8)
        sheet1.write(row_index, 2, seg_result)
        label = '平台'.encode(utf8)
        label_index = 2
        sheet1.write(row_index, 3, label)
        sheet1.write(row_index, 4, label_index)
        row_index += 1

    rows = getRowsFromFile('../txtfiles/qita.txt')
    for sentence in rows:
        if review_set.__contains__(sentence):
            continue
        review_set.add(sentence)
        sheet1.write(row_index, 0, row_index)
        sentence = sentence.rstrip('\n').encode(utf8)
        sheet1.write(row_index, 1, sentence)
        seg_result = getSegment(sentence, stopwordslist)
        seg_result = seg_result.encode(utf8)
        sheet1.write(row_index, 2, seg_result)
        label = '其他'.encode(utf8)
        label_index = 3
        sheet1.write(row_index, 3, label)
        sheet1.write(row_index, 4, label_index)
        row_index += 1

    rows = getRowsFromFile('../txtfiles/yewu.txt')
    for sentence in rows:
        if review_set.__contains__(sentence):
            continue
        review_set.add(sentence)
        sheet1.write(row_index, 0, row_index)
        sentence = sentence.rstrip('\n').encode(utf8)
        sheet1.write(row_index, 1, sentence)
        seg_result = getSegment(sentence, stopwordslist)
        seg_result = seg_result.encode(utf8)
        sheet1.write(row_index, 2, seg_result)
        label = '业务'.encode(utf8)
        label_index = 4
        sheet1.write(row_index, 3, label)
        sheet1.write(row_index, 4, label_index)
        row_index += 1

    xls.close()
    return


def write_into_excel_with_path_and_column_list(column_list, row_index, review_set, sheet1, stopwordslist, label):
    path = '../彩电' + label + '.xlsx'
    tmp = get_sentences_from_excel(path, column_list)
    for sentence, sentiment in tmp:
        review_set.add(sentence[0])
        sheet1.write(row_index, 0, row_index)
        sentence = str(sentence[0]).rstrip('\n').encode(utf8)
        sheet1.write(row_index, 1, sentence)
        seg_result = getSegment(sentence, stopwordslist)  # 分词
        seg_result = seg_result.encode(utf8)
        sheet1.write(row_index, 2, seg_result)
        sheet1.write(row_index, 3, label)
        sentiment = str(sentiment[0]).rstrip('\n').encode(utf8)
        sheet1.write(row_index, 4, sentiment)
        row_index += 1
    return row_index


def form_a_xls_with_every_reviews_and_sentiment_label():
    review_set = set()  # 创建空的集合
    xls = xlsxwriter.Workbook('../labeledreview.xlsx')  # 创建一个excel文件
    xls.encoding = utf8  # 设置编码为utf-8
    sheet1 = xls.add_worksheet('default')  # 创建一个工作表对象
    row_index = 0

    stopwordslist = [line.strip().decode('utf-8') for line in open('../txtfiles/stopword.txt').readlines()]

    row_index = write_into_excel_with_path_and_column_list([3, 4], row_index, review_set, sheet1, stopwordslist,
                                                           label='产品')
    row_index = write_into_excel_with_path_and_column_list([3, 4], row_index, review_set, sheet1, stopwordslist,
                                                           label='业务')
    row_index = write_into_excel_with_path_and_column_list([3, 4], row_index, review_set, sheet1, stopwordslist,
                                                           label='平台')
    row_index = write_into_excel_with_path_and_column_list([3, 4], row_index, review_set, sheet1, stopwordslist,
                                                           label='服务')
    row_index = write_into_excel_with_path_and_column_list([1, 2], row_index, review_set, sheet1, stopwordslist,
                                                           label='其他')
    xls.close()
    return


# get_sentences_from_excel('../comment_origin.xlsx', 'reviews', 1)
# get_sentences_from_excel('../彩电业务.xlsx', 'yewu', 3)
# get_sentences_from_excel('../彩电产品.xlsx', 'chanpin', 3)
# get_sentences_from_excel('../彩电其他.xlsx', 'qita', 1)
# get_sentences_from_excel('../彩电平台.xlsx', 'pingtai', 3)
# get_sentences_from_excel('../彩电服务.xlsx', 'fuwu', 3)

# form_a_xls_with_every_reviews()

form_a_xls_with_every_reviews_and_sentiment_label()
