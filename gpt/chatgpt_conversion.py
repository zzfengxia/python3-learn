#!/usr/bin/env python3
# coding  : utf-8
# @author : Francis.zz
# @date   : 2023-07-28 15:30
# @desc   : 使用网页的session key访问chat gpt

from revChatGPT.V1 import Chatbot
import json

"""
使用 `pip install --upgrade revChatGPT` 安装依赖包
使用文档说明：https://github.com/CoolPlayLin/ChatGPT-Wiki/blob/master/docs/ChatGPT/V1.md
1. 可以使用用户名密码、session_token或者access_token 3种方式访问，但是不能同时存在
config参数：
{
    "email" - "OpenAI 账户邮箱",
    "password" - "OpenAI 账户密码",
    "session_token" - "<session_token>"
    "access_token" - "<access_token>"
    "proxy" - "<proxy_url_string>",
    "paid" - True/False #是不是plus帐户
}
2. 用户名密码方式不支持谷歌和微软账号注册的
3. https://chat.openai.com/api/auth/session 获取access_token。
在chat.openai.com的 cookie 中找到__Secure-next-auth.session-token。access_token和session-token使用一个就行了
"""

chatbot = Chatbot(config=json.load(open("D:\\qiyu-work\\chatgpt_auth.json")))


def start_chat():
    print('Welcome to ChatGPT CLI')
    while True:
        prompt = input('> ')

        response = ""

        for data in chatbot.ask(
                prompt
        ):
            response = data["message"]

        print(response)


if __name__ == "__main__":
    start_chat()
