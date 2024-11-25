#!/usr/bin/env python3
# *_*coding=utf-8
"""
@author : Francis.zz
@date   : 2024-01-17 11:25
@desc   : segement_word.py
"""
import jieba
import jieba.posseg


# 加载自定义词典
jieba.load_userdict('../extra/customdict.txt')

def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='UTF-8').readlines()]
    return stopwords

def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    # 加载停用词
    stopwords = stopwordslist("../extra/stop_word.txt")
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr

if __name__ == '__main__':
    import json

    str = "问:你的手机号。 答:13570800165"
    print(str[11:22])