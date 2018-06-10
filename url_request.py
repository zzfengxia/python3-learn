#!/usr/bin/env python3
# *_*coding=utf-8
# @author : Francis.zz
# @date   : 2018-06-10 15:55
# @desc   : http请求

from urllib import request

import requests
from bs4 import BeautifulSoup


def do_get():
    """
    模拟安卓手机UC浏览器的GET请求
    :rtype: http.client.HTTPResponse
    """

    print('request https://www.baidu.com/')
    req = request.Request("https://www.baidu.com/")
    req.add_header("User-Agent", "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-CN; HTC D820u Build/KTU84P) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.1.0.527 U3/0.8.0 Mobile Safari/534.30")

    with request.urlopen(req) as resp:
        data = resp.read()
        print('Status:', resp.status, resp.reason)
        for k, v in resp.getheaders():
            print('%s: %s' % (k, v))
        print('resp:\n', data.decode('utf-8'))


def do_post():
    """模拟登录csdn网站"""
    print('login in https://www.csdn.net/')
    login_url = 'https://passport.csdn.net/account/login'
    # chrome浏览器
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    # 构造获取session的请求
    session_headers = {'User-Agent': user_agent}
    session = requests.session()
    session_resp = session.get(login_url, headers=session_headers)
    print('get session resp status:', session_resp.status_code)
    # 使用BeautifulSoup解析session html，提取lt,execution参数
    soup = BeautifulSoup(session_resp.text, 'lxml')
    # 使用类似jquery的格式查找html表单数据
    lt = soup.select('input[name="lt"]')[0]['value']
    execution = soup.select('input[name="execution"]')[0]['value']

    # print('lt:%s\nexecution:%s' % (lt, execution))
    # 组装登录数据
    login_data = {
        "username": 'zzfengxia@163.com',
        "password": input('input you csdn password'),
        "lt": lt,
        "execution": execution,
        "_eventId": "submit"
    }

    # 发送post请求
    session_resp = session.post(login_url, data=login_data, headers=session_headers)
    print('login resp status:', session_resp.status_code)

    # 通过get请求，请求个人主页，如果没有登入成功，则会返回登页，登入成功，则会获取到登入的个人信息
    response = session.get('https://my.csdn.net/my/mycsdn', headers=session_headers)
    # 打印响应码
    print('request home resp status:', response.status_code)
    # 将响应结果保存文件
    print(response.text)


def do_handler():
    pass


if __name__ == '__main__':
    # GET, POST, HANDLER
    main = 'POST'

    exe = dict(GET=do_get, POST=do_post, HANDLER=do_handler)

    exe[main].__call__()


