#!/usr/bin/env python3
# *_*coding=utf-8
# @author : Francis.zz
# @date   : 2023-09-26 15:21
# @desc   : crawl_news.py


import json
import re
import traceback
from datetime import datetime

import lxml.html
import pandas as pd
from lxml import etree

from datacollect import cons as ct
from datacollect import news_vars as nv

try:
    from urllib.request import urlopen, Request
except ImportError:
    # python3无法使用urllib2
    from urllib2 import urlopen, Request

def get_latest_news(top=None, plate=None, show_content=False):
    """
        获取即时财经新闻，最新新闻-非当前热搜

    Parameters
    --------
        top:数值，显示最新消息的条数，默认为20条
        show_content:是否显示新闻内容，默认False

    Return
    --------
        DataFrame
            classify :新闻类别
            title :新闻标题
            time :发布时间
            url :新闻链接
            content:新闻内容（在show_content为True的情况下出现）
    """
    top = ct.PAGE_NUM[0] if top is None else top
    plate = 'all' if plate is None else plate
    req_path = nv.LATEST_URL['sina'] % (nv.SINA_NEWS_TYPE[plate], top, _random())
    print(req_path)
    try:
        request = Request(req_path)
        data_str = urlopen(request, timeout=10).read()
        data_str = data_str.decode('utf-8')
        desired_property = None
        data = []
        try:
            data_str.encode('utf-8').decode('utf-8')
            json_data = json.loads(data_str)
            # 获取JSON中的属性
            desired_property = json_data['result']['data']
        except json.JSONDecodeError as e:
            print(f'Error decoding JSON: {e}')
        if desired_property is None:
            return None
        for r in desired_property:
            ctime = datetime.fromtimestamp(int(r['ctime']))
            intime = datetime.fromtimestamp(int(r['intime']))
            #rtstr = datetime.strftime(rt, "%m-%d %H:%M")
            #arow = [r['title'], r['intro'], ctime, intime, r['url']]
            arow = [ctime, intime, r['title'], r['url']]
            if show_content:
                arow.append(latest_content(r['url']))
            data.append(arow)
        df = pd.DataFrame(data, columns=nv.LATEST_COLS_C if show_content else nv.LATEST_COLS)
        return df
    except Exception as er:
        #print(str(er))
        stack_trace = traceback.format_exc()  # 获取堆栈跟踪信息并保存到字符串
        print(stack_trace)  # 现在您可以按需要打印或处理堆栈跟踪信息


def latest_content(url):
    '''
        获取即时财经新闻内容
    Parameter
    --------
        url:新闻链接

    Return
    --------
        string:返回新闻的文字内容
    '''
    try:
        html = lxml.html.parse(url)
        res = html.xpath('//div[@id=\"artibody\"]/p')
        if ct.PY3:
            sarr = [etree.tostring(node).decode('utf-8') for node in res]
        else:
            sarr = [etree.tostring(node) for node in res]
        sarr = ''.join(sarr).replace('&#12288;', '')#.replace('\n\n', '\n').
        html_content = lxml.html.fromstring(sarr)
        content = html_content.text_content()
        return content
    except Exception as er:
        print(str(er))


def get_notices(code=None, date=None):
    '''
    个股信息地雷
    Parameters
    --------
        code:股票代码
        date:信息公布日期

    Return
    --------
        DataFrame，属性列表：
        title:信息标题
        type:信息类型
        date:公告日期
        url:信息内容URL
    '''
    if code is None:
        return None
    symbol = 'sh' + code if code[:1] == '6' else 'sz' + code
    url = nv.NOTICE_INFO_URL%(ct.P_TYPE['http'], ct.DOMAINS['vsf'],
                              ct.PAGES['ntinfo'], symbol)
    url = url if date is None else '%s&gg_date=%s'%(url, date)
    html = lxml.html.parse(url)
    res = html.xpath('//table[@class=\"body_table\"]/tbody/tr')
    data = []
    for td in res:
        title = td.xpath('th/a/text()')[0]
        type = td.xpath('td[1]/text()')[0]
        date = td.xpath('td[2]/text()')[0]
        url = '%s%s%s'%(ct.P_TYPE['http'], ct.DOMAINS['vsf'], td.xpath('th/a/@href')[0])
        data.append([title, type, date, url])
    df = pd.DataFrame(data, columns=nv.NOTICE_INFO_CLS)
    return df


def notice_content(url):
    '''
        获取信息地雷内容
    Parameter
    --------
        url:内容链接

    Return
    --------
        string:信息内容
    '''
    try:
        html = lxml.html.parse(url)
        res = html.xpath('//div[@id=\"content\"]/pre/text()')[0]
        return res.strip()
    except Exception as er:
        print(str(er))


def guba_sina(show_content=False):
    """
       获取sina财经股吧首页的重点消息
    Parameter
    --------
        show_content:是否显示内容，默认False

    Return
    --------
    DataFrame
        title, 消息标题
        content, 消息内容（show_content=True的情况下）
        ptime, 发布时间
        rcounts,阅读次数
    """

    from pandas.io.common import urlopen
    try:
        with urlopen(nv.GUBA_SINA_URL%(ct.P_TYPE['http'],
                                       ct.DOMAINS['sina'])) as resp:
            lines = resp.read()
        html = lxml.html.document_fromstring(lines)
        res = html.xpath('//ul[@class=\"list_05\"]/li[not (@class)]')
        heads = html.xpath('//div[@class=\"tit_04\"]')
        data = []
        for head in heads:
            title = head.xpath('a/text()')[0]
            url = head.xpath('a/@href')[0]
            ds = [title]
            ds.extend(_guba_content(url))
            data.append(ds)
        for row in res:
            title = row.xpath('a[2]/text()')[0]
            url = row.xpath('a[2]/@href')[0]
            ds = [title]
            ds.extend(_guba_content(url))
            data.append(ds)
        df = pd.DataFrame(data, columns=nv.GUBA_SINA_COLS)
        df['rcounts'] = df['rcounts'].astype(float)
        return df if show_content is True else df.drop('content', axis=1)
    except Exception as er:
        print(str(er))


def _guba_content(url):
    try:
        html = lxml.html.parse(url)
        res = html.xpath('//div[@class=\"ilt_p\"]/p')
        if ct.PY3:
            sarr = [etree.tostring(node).decode('utf-8') for node in res]
        else:
            sarr = [etree.tostring(node) for node in res]
        sarr = ''.join(sarr).replace('&#12288;', '')#.replace('\n\n', '\n').
        html_content = lxml.html.fromstring(sarr)
        content = html_content.text_content()
        ptime = html.xpath('//div[@class=\"fl_left iltp_time\"]/span/text()')[0]
        rcounts = html.xpath('//div[@class=\"fl_right iltp_span\"]/span[2]/text()')[0]
        reg = re.compile(r'\((.*?)\)')
        rcounts = reg.findall(rcounts)[0]
        return [content, ptime, rcounts]
    except Exception:
        return ['', '', '0']


def _random():
    import random
    return str(random.random())


if __name__ == '__main__':
    main = ''

    exe = dict()

    exe[main].__call__()
