import argparse
import pandas as pd
import matplotlib.pyplot as plt
from util import config as cf
from util import rw as rw
# import numpy as np


def draw_echarts(pd_data, stock_code, adj):
    from util import echarts as ec
    from util import analysis as an
    new_d = an.arrange_data(pd_data)
    ec.draw_chart(new_d, stock_code, cf.get_config('projectpath', 'path_imgs'), adj=adj)


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

def main(filename, code, style, adj):
    df = rw.load_data(cf.get_config('projectpath', 'path_data')+filename)
    print('=========> Data loaded successfully !!!')

    if style == 'echarts':
        draw_echarts(df, stock_code=code, adj=adj)
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
    args = parser.parse_args()
    # print(bool(args.adj))
    main(args.file, args.code, args.style, bool(args.adj))
    # main('tencent_SZ002594.xlsx', '002594 比亚迪', 'echarts', True)
    # main('tencent_SH688111.xlsx', '000001 上证指数', 'echarts', False)