from typing import List, Sequence, Union
# import os
import numpy as np
import pandas as pd

# Pandas Dataframe -> Dict
def arrange_data(pd_data) -> dict:
    # 根据除权系数对价格数据进行调整，此处固定使用【前复权】
    if pd_data.get('dividend') is not None:
        div_adj = div_adj_cal(pd_data)
        pd_data['open']  = pd_data['open']  / div_adj
        pd_data['close'] = pd_data['close'] / div_adj
        pd_data['low']   = pd_data['low']   / div_adj
        pd_data['high']  = pd_data['high']  / div_adj
    else:
        div_adj = [1 for i in range(len(pd_data['date']))]

    return {
        "date":     pd_data['date'].astype(str).values.tolist(),
        "datas":    pd_data[['open', 'close', 'low', 'high', 'volume']].values.tolist(),
        "open":     pd_data['open'].values.tolist(),
        "close":    pd_data['close'].values.tolist(),
        "low":      pd_data['low'].values.tolist(),
        "high":     pd_data['high'].values.tolist(),
        "vols":     pd_data['volume'].values.tolist(),
        "amount":   pd_data['amount'].values.tolist(),
        "div_adj":  div_adj,
        "turnover": pd_data['volume'].values.tolist() if pd_data.get('turnover') is None else pd_data['turnover'].values.tolist(),
    }

def match_data(pd_data1, pd_data2):
    # 整合两组数据，按照时间取交集，便于后续k线图数据对其
    d_t1 = pd_data1.set_index('date')
    d_t2 = pd_data2.set_index('date')
    common_index = d_t1.index.intersection(d_t2.index)
    d_t1 = d_t1.loc[common_index]
    d_t2 = d_t2.loc[common_index]
    df = d_t1.reset_index(drop=False)
    df2 = d_t2.reset_index(drop=False)
    return df, df2

# 除权系数计算
def div_adj_cal(df):
    div_adj = [1 for i in range(len(df['dividend']))] # 累积除权系数
    ratio = 1
    for i in reversed(range(len(df['dividend']))):
        div_adj[i] = ratio
        # 利用nan值不等于自身进行判断该值是否为NaN，【非NaN】且【非空字符串】
        if not(df.loc[i, "dividend"] != df.loc[i, "dividend"]) and df.loc[i, "dividend"].strip() != '':
            ratio = ratio * float(df.loc[i-1, "close"]) / float(df.loc[i, "open"])    # 简单采用【昨收/今开】作为除权系数

    return div_adj

def cal_macd(price):
    price = pd.DataFrame(price)
    exp12 = price.ewm(span=12, adjust=False).mean()
    exp26 = price.ewm(span=26, adjust=False).mean()
    dif = exp12 - exp26
    dea = dif.ewm(span=9, adjust=False).mean()
    macds = dif - dea
    return {
        "macds": macds[0].values.tolist(),
        "difs": dif[0].values.tolist(),
        "deas": dea[0].values.tolist(),
    }

def cal_macd_adj(price):
    exp12 = price.ewm(span=12, adjust=False).mean()
    exp26 = price.ewm(span=26, adjust=False).mean()
    dif = (exp12 - exp26)/price
    dea = dif.ewm(span=9, adjust=False).mean()
    macds = dif - dea
    return {
        "macds": macds.values.tolist(),
        "difs": dif.values.tolist(),
        "deas": dea.values.tolist(),
    }

def cal_obv(close, volume):
    obv = [0]
    for i in range(len(close)-1):
        if close[i+1]>close[i]:
            obv.append(obv[i]+volume[i+1])
        else:
            obv.append(obv[i]-volume[i+1])
    
    return obv

def cal_bias(price, avgprice):
    return [float("%.4f" % ((p-ap)/ap)) if ap!=None else None for p, ap in zip(price, avgprice)]

def cal_ma(data, day_count: int):
    ma: List[Union[float, str]] = []

    for i in range(len(data)):
        if i < (day_count-1):
            ma.append(None)
            continue
        sum_total = 0.0
        for j in range(day_count):
            sum_total += float(data[i - j])
        ma.append(float("%.4f" % (sum_total / day_count)))
    return ma

def cal_move_std(data, day_count:int):
    std: List[float] = []

    for i in range(len(data)):
        if i < (day_count-1):
            std.append("-")
            continue
        else:
            current_std = np.std(data[(i-day_count+1):i+1])
            std.append(current_std)
    return std
    
def cal_adjprice(amount, volume, day_count: int):
    adjprice: List[Union[float, str]] = []

    for i in range(len(amount)):
        if i < (day_count-1):
            adjprice.append(None)
            continue
        sum_amount = 0.0
        sum_volume = 0.0
        for j in range(day_count):
            sum_amount += float(amount[i - j])
            sum_volume += float(volume[i - j])
        adjprice.append(float("%.4f" % (sum_amount / sum_volume / 100)))
    return adjprice

def cal_adjprice_plus(amount, volume, div_adj, day_count: int):
    adjprice: List[Union[float, str]] = []
    cost_daily_adj = [x/y/z  for x, y, z in zip(amount, volume, div_adj)]  # 计算日内平均交易成本（调整）

    for i in range(len(amount)):
        if i < (day_count-1):
            adjprice.append(None)
            continue
        sum_amount = 0.0    #计算加权分母累积和
        sum_weight = 0.0    #计算加权分子累积和
        for j in range(day_count):
            sum_amount += float(amount[i - j])
            sum_weight += cost_daily_adj[i - j] * float(amount[i - j])
        adjprice.append(float("%.4f" % (sum_weight / sum_amount)))
    return adjprice
# 计算市场买卖势能
# def cal_potential(pd_data):

def cal_emotion(close, amount, volume, div_adj):
    cost_adj = [x/y/z  for x, y, z in zip(amount, volume, div_adj)]  # 计算日内平均交易成本（调整）
    # 收盘价 - 加权成本
    emotion = [(c-p)/c for c, p in zip(close, cost_adj)]
    return emotion

def cal_emotion_v2(high, low, amount, volume, div_adj):
    cost_adj = [x/y/z  for x, y, z in zip(amount, volume, div_adj)]  # 计算日内平均交易成本（调整）
    # 收盘价 - 加权成本
    emotion = [(c-l)/(h-l)*100 if h>l else 100 for h, l, c in zip(high, low, cost_adj)]
    return emotion

def cal_opinion(high, low, amount, volume, div_adj):
    cost_adj = [x/y/z  for x, y, z in zip(amount, volume, div_adj)]  # 计算日内平均交易成本（调整）
    # 收盘价 - 加权成本
    opinion = [(c-l)/(h-l)*100 if h>l else 100 for h, l, c in zip(high, low, cost_adj)]
    return opinion

def cal_opinion2(high, low, close):
    opinion = [(h-l)/c*100 for h, l, c in zip(high, low, close)]
    return opinion

# 计算近N日价格走势的斜率
def cal_slope(close, day_count):
    slope = []
    
    for i in range(len(close)):
        if i < (day_count-1):
            slope.append(0)
            continue

        x = np.array([j for j in range(0,day_count)])
        y = np.array(close[(i+1-day_count):(i+1)])/close[i+1-day_count] #做归一化处理
        coefficients = np.polyfit(x, y, 1)
        slope.append(float(coefficients[0]))
    
    return slope

# 计算近N日价格走势的斜率
def cal_pricediff(close, amount, volume, div_adj, day_count):
    adjprice_moveavg = cal_adjprice_plus(amount, volume, div_adj, day_count)
    close_moveavg = cal_ma(close, day_count)
    vol_movavg = cal_ma(volume, day_count)

    return [(c-p)*v if not isinstance(c, str) else '-' for p,c,v in zip(adjprice_moveavg, close_moveavg, vol_movavg)]
    # return [p-c if not isinstance(p, str) else '-' for p,c in zip(adjprice_moveavg, close_moveavg)]

def cal_test(vols):
    data = pd.DataFrame(vols,columns=['vols'])

    return cal_macd(data['vols'])

# open high close low, sell signal
def cal_ohcl(open, close, low, high, amount, date):
    signal_day = []
    ohcl = []
    for i in range(1, len(open)):
        if open[i] >= close[i-1] and close[i] < close[i-1]:
            strength = abs(float("%.4f" % ((close[i] - open[i])/close[i-1])))
            if strength >= 0.02:
                ohcl.append(high[i]*1.05)#strength
                signal_day.append(date[i])

    return {
        "date": signal_day,
        "value": ohcl,
    }