#!/usr/bin/env python3
# *_*coding=utf-8
"""
@author : Francis.zz
@date   : 2023-11-02 14:09
@desc   : get_stock_eastmoney.py
"""
from datacollect.collect_news.crawl_interface import AbstractStockCrawlData
import requests
from lxml import etree
import pandas as pd
import lxml.html
from pandas import DataFrame
from datacollect import news_vars as nv
from datacollect.util import common_util as cu
import json
import re


class StockCrawlDataEast(AbstractStockCrawlData):
    """
    股票相关接口
    """

    def __init__(self):
        self.source_name = '东财'

    def get_latest_news(self, top=None, plate=None, show_content=False) -> DataFrame:
        """
        获取当前最新新闻
        :param top:             前N条
        :param plate:           板块
        :param show_content:   是否显示具体内容
        :return:
        """
        pass

    def get_hot_news(self, top_n=None, plate=None) -> DataFrame:
        """
        获取当前最新热搜
        :param top_n:           前N条
        :param plate:           板块
        :return:
        """
        pass

    def get_hot_stocks(self, top_n=None) -> DataFrame:
        """
        获取当前最新热搜
        :param top_n:           前N只热度排名最前的股票
        :return:
        """
        pass

    def get_guba_comments(self, stock_code, top_n=None, order_type=None) -> DataFrame:
        """
        获取当前最新热搜
        :param stock_code:      股票代码
        :param top_n:           前N条评论
        :param order_type:      排序方式，最新、最热
        :return:
        """
        return get_comments_from_script(stock_code, top_n, order_type)


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}


def get_comments_from_script(stock_code, top_n=None, order_type=None):
    import traceback

    data = []
    cur_page = 1
    order_type = 'latest' if order_type is None else order_type
    top_n = 30 if top_n is None else top_n
    try:
        while len(data) < top_n:
            # 带“,f”的是最新发帖
            url = nv.GUBA_COMMENT['eastmoney'][order_type] % (stock_code, cur_page)
            print(url)
            response = requests.get(url, headers=nv.DEFAULT_HEADERS)
            html = lxml.html.fromstring(response.text)
            script_tags = html.xpath("//html/body/script")
            for script_tag in script_tags:
                if not script_tag.attrib.get("type"):
                    # 获取没有 type 属性的标签的文本内容
                    script_text = script_tag.text
                    if not script_text:
                        continue
                    if 'article_list' not in script_text:
                        continue
                    start_index = script_text.index('var article_list=') + len('var article_list=')
                    end_index = script_text.index('};', start_index) + 1
                    # 获取var article_list = 之后的json文本
                    article_list_text = script_text[start_index:end_index]
                    # 解析json文本
                    article_list = json.loads(article_list_text)
                    # 反转，最新的放后面
                    comment_list = article_list['re']
                    # 打印 article_list 的值
                    for comment in comment_list:
                        if 'post_title' not in comment:
                            continue
                        title = comment['post_title']
                        author = comment['user_nickname'] if 'user_nickname' in comment else ''
                        time = comment['post_publish_time']
                        reply_num = comment['post_comment_count']
                        read_num = comment['post_click_count']
                        url = comment['post_id']
                        arow = [time, title, author, reply_num, read_num, url]
                        data.append(arow)
            cur_page += 1
        data.reverse()
        df = pd.DataFrame(data[-top_n:], columns=['time', 'title', 'author', 'reply_num', 'read_num', 'url'])
        return df
    except Exception as e:
        print("Error:")
        traceback.print_exc()


def get_overview(stock_code):
    """
    获取即时热度排名

    :param stock_code:
    :return:
    """
    from urllib.parse import quote
    import re
    import json

    headers_cp = headers.copy()
    headers_cp['Content-Type'] = 'application/json'

    data = '{"appKey":"","client":"wap","method":"qgqm","args":{"fundId":"","hkFundId":"","uid":"","customerId":"","custid":"","pageId":"Stock_quotes_page","positions":"Stock_quotes_page_gbxf_text","stockCodeWithoutMarket":"'+stock_code+'","marketCode":0}}'
    encode_data = quote(data)

    url = f'https://eminterservice.securities.eastmoney.com/api/data/companyinfo?data={encode_data}&t={_random()}'
    response = requests.get(url, headers=headers_cp)
    res = response.text
    if not res:
        return None
    # 使用正则表达式提取目标值
    match = re.search(r'\[highlight\](\d+)\[/highlight\]', json.loads(res)['data']['rankInfo']['title'])

    # 如果找到匹配，获取匹配的第一个分组值
    rank_value = match.group(1) if match else None
    return rank_value

def _random():
    import random
    return str(random.random())


def get_comments_from_body(stock_code, date=None, top_n=None, type=None):
    data = []
    try:
        # 带“,f”的是最新发帖
        url = f'https://guba.eastmoney.com/list,{stock_code},f_1.html'
        response = requests.get(url, headers=nv.DEFAULT_HEADERS)
        html = lxml.html.fromstring(response.text)
        tr_list = html.xpath("//tbody[@class='listbody']/tr")
        data = []
        for tr in tr_list:
            title = cu.get_one(tr.xpath('.//div[@class="title"]/a/text()'))
            author = cu.get_one(tr.xpath('.//div[@class="author"]/a/text()'))
            # 发帖时间
            time = cu.get_one(tr.xpath('.//div[@class="update"]/text()'))
            # 阅读数
            read_num = cu.get_one(tr.xpath('.//div[@class="read"]/text()'))
            # 回复数
            reply_num = cu.get_one(tr.xpath('.//div[@class="reply"]/text()'))
            url = cu.get_one(tr.xpath('.//div[@class="title"]/a/@href'))
            arow = [title, author, time, reply_num, read_num, url]
            data.append(arow)
        df = pd.DataFrame(data, columns=['title', 'author', 'time', 'reply_num', 'read_num', 'url'])
        print(df.to_string(col_space=20, index=False, justify='left'))
        return df
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    # with open("C:\\Users\\86153\\Desktop\\1233.txt", 'r', encoding='utf-8') as f:
    #     text = f.read()
    #
    #     html = lxml.html.fromstring(text)
    #     script_tags = html.xpath("//html/body/script")
    #     for script_tag in script_tags:
    #         if not script_tag.attrib.get("type"):
    #             # 获取没有 type 属性的标签的文本内容
    #             script_text = script_tag.text
    #             if not script_text:
    #                 continue
    #             if 'article_list' not in script_text:
    #                 continue
    #             start_index = script_text.index('var article_list =') + len('var article_list =')
    #             end_index = script_text.index('};', start_index) + 1
    #             article_list_text = script_text[start_index:end_index]
    #             # 使用 JSON 解析器解析 script 标签中的文本内容
    #             article_list = json.loads(article_list_text)
    #             # 打印 article_list 的值
    #             for comment in article_list['re']:
    #                 print(comment['post_title'])
    #df = get_comments_from_script('301131', top_n=52)
    #print(df.to_string(col_space=20, index=False, justify='left'))

    rank_value = get_overview('300785')

    # 打印结果
    print(rank_value)
