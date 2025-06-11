import requests, bs4
from datetime import datetime
import os, time
import operator
from itertools import combinations, permutations

"""
@author: Francis.zz
@date: 2023-05-10
@desc: 获取双色球历史开奖信息
"""
class DoubleColorBall(object):
    def __init__(self):
        self.baseUrl = 'http://tubiao.zhcw.com/tubiao/ssqNew/ssqJsp/ssqZongHeFengBuTuAsc.jsp'
        self.dataFile = './balls_data.txt'
        self.lastData = self.load_last()

    def get_html(self, url):
        headers = {
            'Referer': 'https://tubiao.zhcw.com/tubiao/ssqNew/ssqInc/ssqZongHeFengBuTuAscselect=10.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }
        self.session = requests.Session()
        response = self.session.get(url, headers=headers)
        return response.text

    def get_last30(self):
        url = self.baseUrl + '?select=%s' % (30,)
        html = self.get_html(url)
        self.bs = bs4.BeautifulSoup(html, 'html.parser')
        if not self.bs:
            print('fetch data failed')

        data = self.bs.find_all(class_='hgt')
        return self.parse_ball(data)

    def get_all(self, start_year=2003):
        lastYear = datetime.now().year
        for year in range(start_year, lastYear + 1):
            url = self.baseUrl + '?kj_year=%s' % (year,)
            print(url)
            html = self.get_html(url)
            self.bs = bs4.BeautifulSoup(html, 'html.parser')
            if self.bs:
                data = self.bs.find_all(class_='hgt')
                self.save_ball_overwrite(self.parse_ball(data))

    def parse_ball(self, data):
        """
        解析页面信息
        return数据格式：
        期数 日期 红球6个 蓝球1个
        23056 2023-05-18 8 14 15 18 23 33 8
        """
        lotteryData = {}
        for row in data:
            if not isinstance(row, bs4.element.Tag):
                continue
            tag = row.find(class_="qh7").string.strip()
            if tag.startswith("模拟"):
                break
            print(row)
            # 获取a标签的title属性值，<a title="开奖日期：2022-01-01"></a>
            lotteryDate = row.find(class_="qh7").a['title'].strip().replace('开奖日期：', '')
            redBalls = row.find_all(class_="redqiu")
            blueBall = row.find(class_="blueqiu3").string.strip()
            lotteryData[tag] = [lotteryDate] + [r.string for r in redBalls] + [blueBall]
        return lotteryData

    def save_ball(self, data):
        with open(self.dataFile, 'a+') as f:
            for r in sorted(data, reverse=False):  # 升序，最新的数据写在文件最后
                # for r in sorted(data, reverse=True):  #降序
                f.write(str(r) + ' ' + ' '.join(data[r]) + '\n')

    def save_ball_overwrite(self, new_data):
        """
        加载文件已有数据，并去重，重新写入
        :param new_data:
        :return:
        """
        # 加载已有数据
        existing_data = {}
        if os.path.exists(self.dataFile):
            with open(self.dataFile, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(" ", maxsplit=1)
                        existing_data[parts[0]] = parts[1]

        # 合并数据（新数据覆盖旧数据）
        add_data_size = 0
        for k, v in new_data.items():
            if k not in existing_data:
                existing_data[k] = ' '.join(v)
                add_data_size += 1

        # 按期号升序排序
        sorted_items = sorted(existing_data.items(), key=lambda x: x[0])

        # 重写文件
        with open(self.dataFile, 'w') as f:
            for period, content in sorted_items:
                f.write(f"{period} {content}\n")
        print(f"所有数据拉取完成，更新{add_data_size}条数据")

    # 从数据文件中加载最新10条数据
    def load_last10(self):
        if not os.path.exists(self.dataFile):
            return []
        with open(self.dataFile, 'r') as f:
            lines = f.readlines()
            return [] if len(lines) <= 0 else [self.__str_to_map(l) for l in lines[-10:]]

    # 从数据文件中加载最新1条数据
    def load_last(self):
        if not os.path.exists(self.dataFile):
            return {}
        with open(self.dataFile, 'rb') as f:
            try:  # catch OSError in case of a one line file
                # whence 的 0 值表示从文件开头起算，1 表示使用当前文件位置，2 表示使用文件末尾作为参考点。
                # f.seek(-2, os.SEEK_END)意思是从末尾往上读2个字节
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            last_line = f.readline().decode()
            return self.__str_to_map(last_line)

    # 更新数据
    def upt_data(self):
        download_data = self.get_last30()
        had_last_period = list(self.lastData.keys())[0]
        # 筛选key大于某个值的数据
        new_data = {k: v for k, v in download_data.items() if k > had_last_period}
        if len(new_data) == 0:
            print("数据更新失败，请尝试重新下载数据")
            return
        print('更新%s条数据' % (len(new_data)))
        self.save_ball(new_data)

    @staticmethod
    def __str_to_map(line):
        new_line = line.strip('\r').strip('\n')
        line_s = new_line.split(" ", maxsplit=1)
        return {line_s[0]: line_s[1].strip('\r').strip('\n')}


if __name__ == '__main__':
    ball = DoubleColorBall()
    ball.upt_data()
    #ball.get_all(2025)