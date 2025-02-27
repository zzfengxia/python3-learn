import warnings

import baostock as bs
import tushare as ts
import qstock as qs
from pandas import DataFrame
import datacollect as dc

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
        look_col = df[['code', 'name', 'price', 'high', 'low', '涨跌幅', 'b1_p', 'b1_v', 'a1_p', 'a1_v']]
        # 列格式化, inplace=True覆盖当前列信息
        look_col = look_col.rename(columns={'code': '代码', 'name': '名称', 'price': '当前价格', 'high': '最高', 'low': '最低'})

        # 格式化输出
        # index: 指定是否包含行索引，默认为 True；
        # justify: 指定数据对齐方式，默认为 'right'，表示右对齐。你可以将其设置为 'left' 或 'center'，实现左对齐或居中对齐。
        print(look_col.to_string(index=False, justify='left', col_space=10))

    def change_format(self, x):
        x = '%.2f' % x

    # 根据名称获取股票代码
    def search_code_by_name(self, name):
        bs.login()
        res = bs.query_stock_basic(code_name=name)
        print(res.get_data())

    def daily_review(self, date):
        ts.set_token("087f32845ee8ad6dada139a193978dcb55d8a6fd18441a23aa9d242b")
        pro = ts.pro_api()
        # 获取当前交易日的股票数据
        today = pro.daily(trade_date=date)

        # 获取当前交易日涨停的股票
        today_up_limit = today[today['pct_change'].apply(lambda x: x >= 9.95)]

        # 获取当前交易日跌停的股票
        today_down_limit = today[today['pct_change'].apply(lambda x: x <= -9.95)]

        # 获取当前交易日连涨天数大于等于3天的股票
        today_continue_up = today[today['pct_change'].apply(lambda x: x >= 0)]['ts_code'].value_counts()[3:]

        # 输出结果
        print('涨幅居前：')
        print(today_up_limit[['ts_code', 'trade_date', 'close', 'pct_change']])
        print('跌幅居前：')
        print(today_down_limit[['ts_code', 'trade_date', 'close', 'pct_change']])
        print('连涨天数大于等于3天：')
        print(today_continue_up)

    def news(self):
        df: DataFrame = dc.get_latest_news(top=10)
        print(df)

"""
DataFrame
属性：代码，名称，涨跌幅，现价，开盘价，最高价，最低价，最日收盘价，成交量，换手率，成交额，市盈率，市净率，总市值，流通市值
"""
#df = ts.get_today_all()

if __name__ == '__main__':
    # 忽略指定警告信息
    # warnings.filterwarnings("ignore", category=FutureWarning)
    quotesWrap = StockQuotesWrap()
    #quotesWrap.search_code_by_name('')
    quotesWrap.get_realtime_quotes((
                                    '600031', '600446', '000799',
                                    '601788', '601990',
                                    '600351', '000011',
                                    '600570', '301131', '002386',
                                    '300364', '300759', '300644',
                                    '300533', '000661', '003000',
                                    '002468', '605136', '300592',
                                    'sh000001', 'sz399001', 'sz399006',
    ))

    #quotesWrap.news()
    #quotesWrap.daily_review('20230926')

    #pro.query()
    #ts.get_day_all()

    # bs.login()
    # data = bs.query_stock_basic("sz.300086")
    # print(data.get_data())
    #news = qs.limit_pool()
    #df=qs.ths_money('概念',n=5)
    #print(df.to_string())

    # 可以获取所有
    # df = qs.market_realtime()
    # print(f'总数量：{len(df)}')
    # print()
    # print(df.to_string())


