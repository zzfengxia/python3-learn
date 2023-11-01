#!/usr/bin/env python3
# *_*coding=utf-8
"""
@author : Francis.zz
@date   : 2023-10-30 17:16
@desc   : my_class.py
"""

from lxml import html

# 获取并执行实现了 MyProtocol 协议的所有类的方法
if __name__ == "__main__":
    # Sample HTML content
    html_content = """
    <tbody>
        <tr class="">
            <td class="td-01"><i class="icon-top"></i></td>
            <td class="td-02">
                <a href="/weibo?q=%23%E9%87%91%E8%9E%8D%E6%98%AF%E5%9B%BD%E6%B0%91%E7%BB%8F%E6%B5%8E%E7%9A%84%E8%A1%80%E8%84%89%23&Refer=new_time" target="_blank">金融是国民经济的血脉</a>
            </td>
            <td class="td-03"><i class="icon-txt icon-txt-hot">热</i></td>
        </tr>
        <tr class="">
            <td class="td-01 ranktop ranktop1">1</td>
            <td class="td-02">
                <a href="/weibo?q=%23%E8%BF%AA%E4%B8%BD%E5%A7%90%E7%83%AD%E4%BA%86%E5%90%A7%23&t=31&band_rank=1&Refer=top" target="_blank">迪丽姐热了吧</a>
                <span>综艺 1204033</span>
            </td>
            <td class="td-03"><i class="icon-txt icon-txt-len-1" style="background-color:#ff3852;">新</i></td>
        </tr>
    </tbody>
    """

    # Parse the HTML content
    tree = html.fromstring(html_content)

    tr = tree.xpath('//tbody/tr')
    for sub in tree.xpath('//tbody/tr'):
        # Use XPath to extract the desired information
        hot_search_rank = sub.xpath('.//td[@class="td-01 ranktop"]/text()[1]')
        keywords = sub.xpath('.//td[@class="td-02"]/a/text()[1]')
        heat_values = sub.xpath('.//td[@class="td-02"]/span/text()[1]')

        # Print the extracted information
        print("Hot Search Rank:", hot_search_rank)
        print("Keywords:", keywords)
        print("Heat Values:", heat_values)



