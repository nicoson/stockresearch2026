import argparse
import datetime
import pandas as pd
from util import config as cf
from util import rw as rw

def fetch_data(market='SH', code=None, source=None, filename=None):
    # 如果有本地文件，则优先加载本地文件。否则再请求在线数据
    df_local = rw.load_data(filename)
    if df_local is not None:
        start_year = int(df_local['date'].iloc[-1][:4])
        df_local = df_local[df_local['date']<str(start_year)]  # 删除最近一年的数据
    else:
        start_year = 1990

    if source == 'tencent' and code != None:
        df_new = fetch_data_tencent(market, code, start_year)
    elif source == 'tushare' and code != None:
        df_new = fetch_data_tushare(market, code, start_year)
    elif source == 'akshare' and code != None:
        df_new = fetch_data_akshare(market, code, start_year)
    else:
        df_new = None
        print('function [get_data]: Parameter error !!!')

    df_new[["open", "close", "high", "low", "volume", "amount", "turnover"]] = df_new[["open", "close", "high", "low", "volume", "amount", "turnover"]].astype(float)
    # df_new[["dividend", "finance"]] = df_new[["dividend", "finance"]].astype(str)
    pd_data = pd.concat([df_local, df_new])
    pd_data = pd_data.reset_index(drop=True)

    print(pd_data.shape)
    return pd_data

def fetch_data_akshare(market='SH', code=None, start_year=1990):
    # 数据来源 https://akshare.akfamily.xyz/
    # 历史数据 https://akshare.akfamily.xyz/data/stock/stock.html#id23
    import akshare as ak
    if market == 'SH' or market == 'SZ':
        # 前复权 adjust="qfq"， 后复权 adjust="hfq"，默认不复权
        # 东方财富数据接口
        pd_data = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=str(start_year)+"0101", end_date='20991231', adjust="qfq")
        # 日期  股票代码  开盘  收盘  最高  最低  成交量  成交额  振幅  涨跌幅  涨跌额  换手率
        pd_data.columns = ['date', 'code', 'open', 'close', 'high', 'low', 'volume', 'amount', 'amplitude', 'pct_chg', 'change', 'turnover']
        del pd_data['code']
    elif market == 'FUND':
        pd_data = ak.fund_etf_hist_em(symbol=code, period="daily", start_date=str(start_year)+"0101", end_date='20991231', adjust="qfq")
        # 日期  开盘  收盘  最高  最低  成交量  成交额  振幅  涨跌幅  涨跌额  换手率
        pd_data.columns = ['date', 'open', 'close', 'high', 'low', 'volume', 'amount', 'amplitude', 'pct_chg', 'change', 'turnover']
        
    pd_data.set_index('date', drop=False, inplace=True)
    return pd_data

def fetch_data_tushare(market='SH', code=None, start_year=1990):
    # 数据来源 https://tushare.pro/
    import tushare as ts
    pro = ts.pro_api(cf.get_config('datatoken', 'token_tushare'))
    if market == 'SH' or market == 'SZ':
        # pd_data = pro.query('daily', ts_code = code+'.'+market)
        pd_data = pro.daily(ts_code=code+'.'+market, start_date=str(start_year)+'0101', end_date='20991231')
        pd_data.columns = ['code', 'date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'volume', 'amount']
        pd_data['amount'] = pd_data['amount']*1000
        pd_data = pd_data.sort_values(by='date', ascending=True)
        del pd_data['code']
    elif market == 'FUND':
        pd_data = pro.fund_daily(ts_code=code+'.'+market, start_date=str(start_year)+'0101', end_date='20991231')
        pd_data.columns = ['code', 'date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'volume', 'amount']
        del pd_data['code']
    pd_data.set_index('date', drop=False, inplace=True)
    return pd_data

def fetch_data_tencent(market='SH', code='588000', start_year=1990):
    # 数据来源 https://proxy.finance.qq.com/cgi/cgi-bin/stockinfoquery/kline/app/get?code=sz002594&fromDate=2024-01-01&toDate=2025-12-31&ktype=day&limit=800
    import requests
    url_base = cf.get_config('datasource', 'url_tencent')
    data = []
    step = 5
    for i in range(start_year, datetime.datetime.now().year+1, step):
        if i > datetime.datetime.now().year:
            break

        url = url_base+market.lower()+code+'&fromDate='+str(i)+'-01-01&toDate='+str(i+step-1)+'-12-31&ktype=day&limit=1900'
        res = requests.get(url)

        # 检查请求是否成功
        if res.status_code == 200:
            # 成功获取数据，可以处理返回的内容
            res_data = res.json()
            data = data + res_data['data']['nodes']  # 如果返回的是JSON数据，可以使用json()方法解析

    df = pd.DataFrame(data)
    df.columns = ["open", "close", "high", "low", "volume", "amount", "turnover", "turnover_raw", "date", "div_adj", "tradeDays", "dividend", "addZdf", "finance"]
    del df['turnover_raw']
    del df['div_adj']
    del df['tradeDays']
    del df['addZdf']
    df = df.reindex(columns=["date", "open", "close", "high", "low", "volume", "amount", "turnover","dividend", "finance"])
    # df = div_adj_cal(df)
    return df

def main(market, code, source):
    filename = cf.get_config('projectpath', 'path_data')+source+'_'+market+code+'.xlsx'
    df = fetch_data(market, code, source, filename=filename)
    rw.write_data(df, filename)
    print(df)


# example: python download_data.py --market=SH --code=588000 --source=tencent
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--market', type=str, default='SH', help='stock market[SH, SZ, BJ, FUND]')
    parser.add_argument("--code", type=str, default='688981', help='stock symbol/code')
    parser.add_argument('--source', default='tencent', help='data source[tencent, akshare, tushare]')
    args = parser.parse_args()

    main(args.market, args.code, args.source)
    # main('SZ', '002594', 'tencent')