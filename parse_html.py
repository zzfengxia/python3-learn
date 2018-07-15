#!/usr/bin/env python3
# *_*coding=utf-8
# @author : Francis.zz
# @date   : 2018-06-11 21:27
# @desc   : 解析html页面
from html.parser import HTMLParser
from html.entities import name2codepoint


class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print('<%s>' % tag)

    def handle_endtag(self, tag):
        print('</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        """类似<br/>的标签"""
        print('<%s/>' % tag)

    def handle_data(self, data):
        print(data)

    def handle_comment(self, data):
        """ 注释 """
        print('<!--', data, '-->')

    def handle_entityref(self, name):
        print('&%s;' % name)

    def handle_charref(self, name):
        print('&#%s;' % name)


def parse_html(html):
    parser = MyHTMLParser()
    parser.feed(html)


if __name__ == '__main__':
    html = '''<html>
        <head></head>
        <body>
        <!-- test html parser -->
            <p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p>
            <br/>
        </body></html>'''

    main = 'PARSE_HTML'

    exe = dict(PARSE_HTML=parse_html)

    exe[main].__call__(html)
