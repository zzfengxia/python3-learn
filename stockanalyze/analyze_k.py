import akshare as ak
import pandas as pd
from datetime import datetime


class StockAnalyzeWrap(object):
    def __init__(self):
        print()

    def get_all_stocks(self):
        """获取A股股票代码列表"""
        df = ak.stock_info_a_code_name()
        return df['code'].tolist()


    def get_all_no_st_stocks(self) -> pd.DataFrame:
        """
        沪深非ST股票合集
        :return: 沪深 A 股数据
        :rtype: pandas.DataFrame
        """
        big_df = pd.DataFrame()
        stock_sh = ak.stock_info_sh_name_code(symbol="主板A股")
        stock_sh = stock_sh[["证券代码", "证券简称"]]

        stock_sz = ak.stock_info_sz_name_code(symbol="A股列表")
        stock_sz["A股代码"] = stock_sz["A股代码"].astype(str).str.zfill(6)
        big_df = pd.concat(
            objs=[big_df, stock_sz[["A股代码", "A股简称"]]], ignore_index=True
        )
        big_df.columns = ["证券代码", "证券简称"]

        stock_kcb = ak.stock_info_sh_name_code(symbol="科创板")
        stock_kcb = stock_kcb[["证券代码", "证券简称"]]

        big_df = pd.concat(objs=[big_df, stock_sh], ignore_index=True)
        big_df = pd.concat(objs=[big_df, stock_kcb], ignore_index=True)
        big_df.columns = ["code", "name"]
        big_df = big_df[~big_df['name'].str.contains("ST", case=False)]

        return big_df['code'].tolist()


    def get_kline(self, code, start_date=None):
        """获取某股票指定时间段的K线数据"""
        try:
            df = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="qfq", start_date=start_date)
            df['date'] = pd.to_datetime(df['日期'])
            df = df.sort_values('date').reset_index(drop=True)
            return df
        except Exception as e:
            print(f"{code} 获取失败：{e}")
            return pd.DataFrame()

    def get_prev_trade_day(self, date_str: str) -> str:
        """
        获取指定日期之前的最近一个交易日（yyyyMMdd 格式）
        """
        # 将字符串转换为 datetime.date 类型
        target_date = datetime.strptime(date_str, "%Y%m%d").date()

        # 获取交易日历（Sina版本）
        trade_cal_df = ak.tool_trade_date_hist_sina()

        # 过滤早于当前日期的所有交易日
        trade_cal_df = trade_cal_df[trade_cal_df['trade_date'] < target_date]

        if not trade_cal_df.empty:
            prev_trade_date = trade_cal_df.iloc[-1]['trade_date']
            return prev_trade_date.strftime("%Y%m%d")
        else:
            return None


    def has_unfilled_gap(self, df, gap_date_str="20250407"):
        """判断是否在gap_date出现缺口，且未回补"""
        df = df.sort_values("date")
        gap_date = pd.to_datetime(gap_date_str)
        # 上一个交易日
        prev_date = pd.to_datetime(self.get_prev_trade_day(gap_date_str))

        if gap_date not in df['date'].values or prev_date not in df['date'].values:
            return False

        prev_day = df[df['date'] == prev_date].iloc[0]
        gap_day = df[df['date'] == gap_date].iloc[0]

        # 向上跳空
        if gap_day['最低'] > prev_day['最高']:
            # 检查后续是否回补（低于 prev_day 高点）
            after = df[df['date'] > gap_date]
            if not after.empty and (after['最低'] < prev_day['最高']).any():
                return False
            return True

        # 向下跳空
        if gap_day['最高'] < prev_day['最低']:
            after = df[df['date'] > gap_date]
            if not after.empty and (after['最高'] > prev_day['最低']).any():
                return False
            return True

        return False

    def scan_unfilled_gap(self, code=None, gap_date_str="20250407"):
        """
        扫描所有未回补指定日期缺口的股票代码
        :param code: 不指定则扫描全部
        :param gap_date_str:
        :return:
        """
        if code is None:
            codes = self.get_all_no_st_stocks()
        else:
            codes = [code]
        result = []
        print(f"扫描非ST股票数量：{len(codes)}")
        for code in codes:
            print(f"检查股票：{code}")
            prev_day = self.get_prev_trade_day(gap_date_str)
            df = self.get_kline(code, start_date=prev_day)
            if df.empty:
                continue
            if self.has_unfilled_gap(df, gap_date_str):
                result.append(code)
        print(f"\n找到未补缺口的股票共 {len(result)} 只：")
        print(result)
        return result


if __name__ == '__main__':
    analyze = StockAnalyzeWrap()
    #print(f'共有{len(analyze.get_all_no_st_stocks())}只股票')
    #print(analyze.get_prev_trade_day("20250407"))
    #print(analyze.get_kline('300785', start_date="20250407").to_string())
    analyze.scan_unfilled_gap('600570')
