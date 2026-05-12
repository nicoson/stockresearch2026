# 宏观经济形势观察：
#   使用市场融资/融券数据，对比大盘指数走势，分析两者间的关系

import argparse
from util import config as cf
from util import rw as rw
from util import analysis as ana
from util import charts as charts
from pyecharts import options as opts
# import numpy as np

def draw_chart(pd_data, title, pd_data2):
    kdata = ana.arrange_data(pd_data)
    kline = charts.k_line(kdata, title, cid=0, adj=False)    # k 线图

    ratio = pd_data2['rzye'] / pd_data2['rqylje']
    ratio_bar = charts.draw_bar(pd_data2['date'].values.tolist(), ratio.values.tolist(), '融资融券比率', title_pos=490, itemstyle_opts='', cid=1)
    rzye_bar = charts.draw_bar(pd_data2['date'].values.tolist(), (pd_data2['rzye']/100000000).values.tolist(), '融资余额（亿元）', title_pos=620, itemstyle_opts='', cid=2)
    rqylje_bar = charts.draw_bar(pd_data2['date'].values.tolist(), (pd_data2['rqylje']/100000000).values.tolist(), '融券余量金额（亿元）', title_pos=750, itemstyle_opts='', cid=3)
    
    grid_chart = charts.new_grid(1000,1200)
    grid_chart.add(
        kline,
        grid_opts=opts.GridOpts(pos_left="7%", pos_right="1%", height="350px"),
    )

    grid_chart.add(
            ratio_bar,
            grid_opts=opts.GridOpts(pos_left="7%", pos_right="1%", pos_top="490px", height="100px"),
    )

    grid_chart.add(
            rzye_bar,
            grid_opts=opts.GridOpts(pos_left="7%", pos_right="1%", pos_top="620px", height="100px"),
    )

    grid_chart.add(
            rqylje_bar,
            grid_opts=opts.GridOpts(pos_left="7%", pos_right="1%", pos_top="750px", height="100px"),
    )

    savedir = cf.get_config('projectpath', 'path_imgs')
    charts.save_grid(grid_chart, "macro_chart_" + title + ".html", savedir)


def main(filename, title):
    df = rw.load_data(cf.get_config('projectpath', 'path_data')+filename)
    df2 = rw.load_data(cf.get_config('projectpath', 'path_data')+'SSE_RZRQ_.xlsx')
    df,df2 = ana.match_data(df,df2)
    print('=========> Data init successfully !!!')

    draw_chart(df, title, df2)


# example: python candle.py --style=pyplot --file=akshare_SH688981.xlsx --code=688981
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('--file', type=str, default='akshare_SH688981.xlsx', help='stock data filename')
    # parser.add_argument("--code", type=str, default='688981', help='stock symbol/code')
    # parser.add_argument("--style", type=str, default='echarts', help='draw method[echarts/pyplot]')
    # parser.add_argument("--adj", type=int, default=1, help='add adjusted trade price')
    # parser.add_argument('--file2', type=str, default=None, help='compare stock data filename')
    # parser.add_argument("--code2", type=str, default=None, help='compare stock symbol/code')
    # args = parser.parse_args()
    filename = 'tencent_SH000001.xlsx'
    title = '000001 上证指数'
    # main(args.file, args.code, args.style, bool(args.adj), args.file2 if args.file is not None else None, args.code2 if args.code2 is not None else None)
    main(filename, title)