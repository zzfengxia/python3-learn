#!/usr/bin/env python3
# *_*coding=utf-8
# @author : Francis.zz
# @date   : 2018-06-10 21:47
# @desc   : 使用SAX解析xml

from xml.parsers.expat import ParserCreate


class DefaultSaxHandler(object):
    def __init__(self):
        """记录当前标签"""
        self.__cur_tag__ = None

    def start_element(self, name, attrs):
        """attrs 属性默认是一个dict"""
        print('sax:start_element: %s, attrs: %s' % (name, str(attrs)))
        self.__cur_tag__ = name
        if self.__cur_tag__ == 'a':
            href = attrs['href']
            print('a标签的href:', href)

    def end_element(self, name):
        print('sax:end_element: %s' % name)

    def char_data(self, text):
        print('sax:char_data: %s' % text)


def parse_xml():
    xml = r'''<?xml version="1.0"?>
    <ol>
        <li><a href="/python">Python</a></li>
        <li><a href="/ruby">Ruby</a></li>
    </ol>
    '''
    handler = DefaultSaxHandler()
    parser = ParserCreate()
    parser.StartElementHandler = handler.start_element
    parser.EndElementHandler = handler.end_element
    parser.CharacterDataHandler = handler.char_data
    parser.Parse(xml)


if __name__ == '__main__':
    # PARSE_XML
    main = 'PARSE_XML'

    exe = dict(PARSE_XML=parse_xml)

    exe[main].__call__()
