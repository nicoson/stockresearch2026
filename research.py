import pandas as pd
import matplotlib.pyplot as plt
from util import config as cf
from util import rw as rw
import numpy as np
# import sys
# sys.path.append(cf.get_config('projectpath', 'path_util'))
from util import analysis as ana

TREND_DOWN = pd.DataFrame([
    ['2020-08-05','2020-09-30'],
    ['2020-11-09','2020-12-28'],
    ['2020-01-14','2021-02-09'],
    ['2021-06-30','2021-07-21'],
    ['2021-08-06','2022-04-26'],##
    ['2022-06-28','2022-08-02'],
    ['2022-08-02','2022-10-12'],
    ['2023-04-21','2023-08-14'],##
    ['2023-09-05','2023-09-20'],
    ['2023-11-02','2024-02-05'],##
    ['2024-03-18','2024-04-15'],
    ['2024-07-22','2024-09-13'],
    ['2024-11-08','2024-12-17'],
    ['2025-02-21','2025-06-23'],##
    ['2025-10-09','2025-12-16']##
], columns=['begin', 'end'])
    
TREND_UP = pd.DataFrame([
        ['2020-09-30','2020-11-09'],##
        ['2020-12-28','2021-01-14'],
        ['2021-07-21','2021-08-06'],
        ['2022-04-26','2022-06-28'],##
        ['2023-03-13','2023-04-21'],
        ['2023-08-14','2023-09-05'],
        ['2023-09-20','2023-11-02'],
        ['2024-02-05','2024-03-18'],
        ['2024-04-15','2024-07-22'],##
        ['2024-09-13','2024-11-08'],##
        ['2024-12-17','2025-02-21'],##
        ['2025-08-13','2025-10-09']
    ], columns=['begin', 'end'])

TREND_CONSOLID = pd.DataFrame([   
    ['2021-02-09','2021-06-17'],##
    ['2022-10-28','2023-03-13'],##
    ['2025-06-23','2025-08-13']
], columns=['begin', 'end'])


def draw_pyplot(pd_data, stock_code):
    # pd_data = pd_data.set_index('date')
    ydata = pd_data['volume']
    low = pd_data['low']
    high = pd_data['high']
    xdata = [(h-l)/l*100 for l,h in zip(low,high)]

    x = []
    y = []
    for i in range(len(xdata)):
        if i < (20-1):
            continue
        else:
            if ydata.iloc[i] == max(ydata[(i-20+1):(i+1)]):
                x.append(xdata[i])
                y.append(ydata.iloc[i])

    plt.plot(x, y, 'bo')
    plt.title(stock_code)
    plt.xlabel("price diversity")
    plt.ylabel("volume")
    plt.show()

def draw_kline(pd_data, stock_code):
    import mplfinance as mpf
    
    pd_data['date']=pd.to_datetime(pd_data['date'])
    pd_data = pd_data.set_index('date')
    # fig = plt.figure()
    mpf.plot(
        data=pd_data[['open', 'high', 'low', 'close', 'volume']],
        volume=True,
        mav=(5, 20, 60, 120, 240),
        type="candle",
        title=stock_code,
        # ylabel="price($)",
        style="binance",
        figratio=(12, 6)
    )
    plt.show()

def main(filename, code):
    df = rw.load_data(cf.get_config('projectpath', 'path_data')+filename)
    # draw_pyplot(df, code)
    draw_kline(df, code)
    

# example: python candle.py --style=pyplot
if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--file', type=str, default='akshare_SH688981.xlsx', help='stock data filename')
    # parser.add_argument("--code", type=str, default='688981', help='stock symbol/code')
    # args = parser.parse_args()
    file = 'tencent_SH688981.xlsx'
    code = '588000 科创50ETF'
    main(file, code)