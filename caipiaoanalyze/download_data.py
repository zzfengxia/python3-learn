import requests, bs4
from datetime import datetime
import os, time
import operator
from itertools import combinations, permutations


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

    def get_all(self):
        lastYear = datetime.now().year
        for year in range(2003, lastYear + 1):
            url = self.baseUrl + '?kj_year=%s' % (year,)
            print(url)
            html = self.get_html(url)
            self.bs = bs4.BeautifulSoup(html, 'html.parser')
            if self.bs:
                data = self.bs.find_all(class_='hgt')
                self.save_ball(self.parse_ball(data))

    # 解析页面信息
    def parse_ball(self, data):
        lotteryData = {}
        for row in data:
            if not isinstance(row, bs4.element.Tag):
                continue
            tag = row.find(class_="qh7").string.strip()
            if tag.startswith("模拟"):
                break
            # 获取a标签的title属性值，<a title="开奖日期：2022-01-01"></a>
            lotteryDate = row.find(class_="qh7").a['title'].strip().replace('开奖日期：', '')
            redBalls = row.find_all(class_="redqiu")
            blueBall = row.find(class_="blueqiu3").string.strip()
            lotteryData[tag] = [lotteryDate] + [r.string for r in redBalls] + [blueBall]
        return lotteryData

    def save_ball(self, data):
        with open(self.dataFile, 'a+') as f:
            for r in sorted(data, reverse=False):  #升序，最新的数据写在文件最后
            # for r in sorted(data, reverse=True):  #降序
                f.write(str(r) + ' ' + ' '.join(data[r]) + '\n')

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