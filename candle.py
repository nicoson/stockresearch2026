import argparse
import pandas as pd
import matplotlib.pyplot as plt
from util import config as cf
from util import rw as rw
from util import analysis as ana
# import numpy as np


def draw_echarts(pd_data, stock_code, adj, df2=None, c2=None):
    from util import charts as charts
    from util import analysis as an
    new_d = an.arrange_data(pd_data)
    new_d2 = None if df2 is None else an.arrange_data(df2)
    charts.draw_chart(new_d, stock_code, cf.get_config('projectpath', 'path_imgs'), adj=adj, data2=new_d2, c2=c2)


def draw_pyplot(pd_data, stock_code, start_time='2024-06-01', end_time='2025-12-31'):
    import mplfinance as mpf
    
    pd_data['date']=pd.to_datetime(pd_data['date'])
    pd_data = pd_data.set_index('date')
    data = pd_data.loc[start_time:end_time]
    # fig = plt.figure()
    mpf.plot(
        data=data[['open', 'high', 'low', 'close', 'volume']],
        volume=True,
        mav=(5, 20, 60, 120, 240),
        type="candle",
        title=stock_code,
        # ylabel="price($)",
        style="binance",
        figratio=(12, 6)
    )
    plt.show()

def main(filename, code, style, adj, f2=None, c2=None):
    df = rw.load_data(cf.get_config('projectpath', 'path_data')+filename)
    print('=========> Main Data loaded successfully !!!')
    df2 = None
    if f2 != None:
        df2 = rw.load_data(cf.get_config('projectpath', 'path_data')+f2)
        print('=========> Compare Data loaded successfully !!!')
        # 整合两组数据，按照时间取交集，便于后续k线图数据对其
        df,df2 = ana.match_data(df,df2)
        print('=========> Data Match successfully !!!')

    if style == 'echarts':
        draw_echarts(df, stock_code=code, adj=adj, df2=df2, c2=c2)
    elif style == 'pyplot':
        draw_pyplot(df, stock_code=code)
    else:
        print('==========>  wrong drawing method !!!')


# example: python candle.py --style=pyplot --file=akshare_SH688981.xlsx --code=688981
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default='akshare_SH688981.xlsx', help='stock data filename')
    parser.add_argument("--code", type=str, default='688981', help='stock symbol/code')
    parser.add_argument("--style", type=str, default='echarts', help='draw method[echarts/pyplot]')
    parser.add_argument("--adj", type=int, default=1, help='add adjusted trade price')
    parser.add_argument('--file2', type=str, default=None, help='compare stock data filename')
    parser.add_argument("--code2", type=str, default=None, help='compare stock symbol/code')
    args = parser.parse_args()
    # print(bool(args.adj))
    # print(args.file2)
    main(args.file, args.code, args.style, bool(args.adj), args.file2 if args.file is not None else None, args.code2 if args.code2 is not None else None)
    # main('tencent_SZ002594.xlsx', '002594 比亚迪', 'echarts', True)
    # main('tencent_SH688111.xlsx', '000001 上证指数', 'echarts', False)
    # main('tencent_SZ002594.xlsx', '002594 比亚迪', 'echarts', True, 'tencent_SH000001.xlsx', '000001 上证指数')