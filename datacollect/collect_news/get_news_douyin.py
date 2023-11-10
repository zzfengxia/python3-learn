#!/usr/bin/env python3
# *_*coding=utf-8
"""
@author : Francis.zz
@date   : 2023-10-30 16:43
@desc   : get_news_douyin.py
"""

import pandas as pd
import requests

from datacollect import news_vars as nv
from datacollect.collect_news.crawl_interface import AbstractNewsCrawlData
import urllib.parse

class NewsCrawlDataDY(AbstractNewsCrawlData):
    def __init__(self):
        self.source_name = '抖音'

    def get_latest_news(self, top=None, plate=None, show_content=False) -> pd.DataFrame:
        pass

    def get_hot_news(self, top_n=None, plate=None) -> pd.DataFrame:
        self.source_name = '抖音热榜'
        return get_hot_news(top_n, plate)

hot_url = 'https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&detail_list=1&source=6&board_type=0&board_sub_type=&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=118.0.0.0&browser_online=true&engine_name=Blink&engine_version=118.0.0.0&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=0&webid=7296409837335201332&msToken=KFgvvIzGHiE-KUuUaqIgcaAsNiXsU_o4bJ0Qp-0RHoWZM6dlnrAr79c-ACs7QP2scmfoiOGSiHIJgZdFL6fBUNoAspLPJkBu4k8HwWDZIbg2f_ZZaRa9&X-Bogus=DFSzswVLq5xANj2mtF-X2F9WX7rr'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Cookie': '__live_version__=%221.1.0.8126%22; odin_tt=d6dde067dd226676c75aad96b3382a9613f11268449ab3761398b68664ff8b9abd70c772343f770e8a6dce8b8c375879bc70b9aa4a4fdf0cdd5e8bd3c2388879741375949052750fd5835d690c2f14dd; ttwid=1%7CaQ6nphMO2Be1RbMEYV5KtiNHx2YTojLH7bcH7v0wr0w%7C1698827810%7C79d295d728ea24b8ef58c6aa3a5fc8b093a0e5200f7e7de10ec915ba89e231b7; webcast_local_quality=null; passport_csrf_token=44318e9fa63699212a59af967572d72a; passport_csrf_token_default=44318e9fa63699212a59af967572d72a; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; strategyABtestKey=%221698827813.042%22; s_v_web_id=verify_lofi7tvw_iGMeDrug_K7Fz_4NK4_BvQP_WC3liHH8lsWk; __ac_nonce=065420e2c0087d45b7a0f; __ac_signature=_02B4Z6wo00f01YQixtwAAIDBBCA8nRvLANGEAsJAAARLsQNwLjXChL4d4JCpHiOFjz6a28YWNQsCnE56KBLbW-8hdxnd319kvg9GgwbeGo0JPpi1Rwky.2sEwqjW.tof.oYgVpRe.MDtWGDK3e; SEARCH_RESULT_LIST_TYPE=%22single%22; download_guide=%221%2F20231101%2F0%22; pwa2=%221%7C0%7C1%7C0%22; douyin.com; device_web_cpu_core=8; device_web_memory_size=8; architecture=amd64; IsDouyinActive=true; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A8%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A0%7D%22; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1699433301012%2C%22type%22%3A1%7D; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; csrf_session_id=b95d0cbb50f0c9f8e18a48d2dbfacd99; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCQW9yTUx5czJHeEt3akFKNEZKajMzaTMzN25RaEgyeGo1V1NkRURzWlN0S1paY0M3NDRBY01uZmc2OXBPRjQrd1lGb1EzVFc4enQrbmg5amV3UHppN3M9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; home_can_add_dy_2_desktop=%221%22; msToken=fvt2MXYD38y2e_i8YtHOGtwqwopgKynWq0puayZ9TobagYkkt3b9dhW6JOASB8iumRaVZ1tofX22B2OmnqU3_Yg7uvthLZUF-eSj3mHEWncn6CRpQaE7; tt_scid=EnZEi8SUE599MJLuxdweawI2TQJidndPwl36EjpbbgSrByvHeNeqJgMoCsraNn63f1b6; msToken=KFgvvIzGHiE-KUuUaqIgcaAsNiXsU_o4bJ0Qp-0RHoWZM6dlnrAr79c-ACs7QP2scmfoiOGSiHIJgZdFL6fBUNoAspLPJkBu4k8HwWDZIbg2f_ZZaRa9'
}
def get_hot_news(top_n=None, plate=None):
    '''
        获取即时热搜
    Parameter
    --------
        top_n: 指定条数
        plate: 板块
    Return
    --------
        DataFrame
            rank:       排名
            keywords :  热搜关键词
            tag:        标签
            heat:       热值
            url :       链接
    '''
    top_n = nv.MAX_HOT_NUM if top_n is None else top_n
    top_n = nv.MAX_HOT_NUM if top_n > nv.MAX_HOT_NUM else top_n
    try:
        response = requests.get(hot_url, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        word_list = json_data['data']['word_list']
        data = []
        for row in word_list:
            if 'position' not in row:
                continue
            rank = row['position']
            keywords = row['word']
            tag = ''
            heat = row['hot_value']
            url = f'https://www.douyin.com/hot/{row["sentence_id"]}/{urllib.parse.quote(keywords)}'
            arow = [rank, keywords, tag, heat, url]
            data.append(arow)
            if len(data) >= top_n:
                break
        df = pd.DataFrame(data, columns=nv.HOT_NEWS_COLS)
        return df
    except Exception as e:
        print(f"Error: {e}")

def _random():
    import random
    return str(random.random())


def get_one(values: tuple):
    return values[0] if values else ''
