import warnings

import baostock as bs
import tushare as ts
from pandas import DataFrame


class StockQuotesWrap(object):
    def __init__(self):
        print()

    def get_realtime_quotes(self, symbols):
        # 实时交易数据
        # 返回值类型提示
        df: DataFrame = ts.get_realtime_quotes(symbols)
        # 将字符串类型的列转换为浮点数类型
        df['price'] = df['price'].astype(float)
        df['pre_close'] = df['pre_close'].astype(float)
        # 计算涨跌幅
        df['涨跌幅'] = (df['price'] - df['pre_close']) / df['pre_close'] * 100
        df['涨跌幅'] = df['涨跌幅'].map(lambda x: '%.2f' % x).astype(float)
        # 截取指定列
        look_col = df[['name', 'price', 'high', 'low', '涨跌幅', 'b1_p', 'b1_v', 'a1_p', 'a1_v']]
        # 列格式化, inplace=True覆盖当前列信息
        look_col = look_col.rename(columns={'name': '名称', 'price': '当前价格', 'high': '最高', 'low': '最低'})

        # 格式化输出
        # index: 指定是否包含行索引，默认为 True；
        # justify: 指定数据对齐方式，默认为 'right'，表示右对齐。你可以将其设置为 'left' 或 'center'，实现左对齐或居中对齐。
        print(look_col.to_string(index=False, justify='left'))

    def change_format(self, x):
        x = '%.2f' % x

    # 根据名称获取股票代码
    def search_code_by_name(self, name):
        bs.login()
        res = bs.query_stock_basic(code_name=name)
        print(res.get_data())

"""
DataFrame
属性：代码，名称，涨跌幅，现价，开盘价，最高价，最低价，最日收盘价，成交量，换手率，成交额，市盈率，市净率，总市值，流通市值
"""
#df = ts.get_today_all()

if __name__ == '__main__':
    # 忽略指定警告信息
    warnings.filterwarnings("ignore", category=FutureWarning)
    quotesWrap = StockQuotesWrap()
    #quotesWrap.search_code_by_name('医药指数')
    quotesWrap.get_realtime_quotes(('sh000001', 'sz399001', 'sz399006',
                                    '301001', '300086', '300570', '300403', '300814', '300147', '002468', '600502'))

    # bs.login()
    # data = bs.query_stock_basic("sz.300086")
    # print(data.get_data())


