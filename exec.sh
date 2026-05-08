#!/bin/bash
# help -n
#          all: 下载数据，并更新图表
#     download: 仅下载数据
#       update: 仅更新图表
# 
# example：sh exec.sh -n update

while getopts n:a: opt
do 
    case "${opt}" in
        n) type=${OPTARG};;
        a) test=${OPTARG};;
    esac
done


if [ "$type" == "all" -o "$type" == "download" ] ; then
    echo "starting download data ...";
    python download_data.py --market=SH --code=000001 --source=tencent  #上证指数
    python download_data.py --market=SH --code=510050 --source=tencent  #华夏上证50ETF
    python download_data.py --market=SH --code=588000 --source=tencent  #科创50ETF
    python download_data.py --market=SH --code=688981 --source=tencent  #中芯国际-科创50
    python download_data.py --market=SH --code=688256 --source=tencent  #寒武纪
    python download_data.py --market=SH --code=688802 --source=tencent  #沐曦股份
    python download_data.py --market=SH --code=688111 --source=tencent  #金山办公
    python download_data.py --market=SZ --code=159915 --source=tencent  #易方达创业板ETF
    python download_data.py --market=SH --code=516160 --source=tencent  #新能源ETF
    python download_data.py --market=SZ --code=159857 --source=tencent  #光伏ETF
    python download_data.py --market=SZ --code=300102 --source=tencent  #乾照光电
    python download_data.py --market=SH --code=600089 --source=tencent  #特变电工-光伏
    python download_data.py --market=SH --code=512400 --source=tencent  #南方中证申万有色金属ETF
    python download_data.py --market=SZ --code=002460 --source=tencent  #赣锋锂业
    python download_data.py --market=SH --code=600547 --source=tencent  #山东黄金
    python download_data.py --market=SZ --code=000807 --source=tencent  #云铝股份
    python download_data.py --market=SZ --code=002428 --source=tencent  #云南锗业
    python download_data.py --market=SZ --code=159824 --source=tencent  #博时新能源汽车ETF
    python download_data.py --market=SZ --code=002594 --source=tencent  #比亚迪
    python download_data.py --market=SZ --code=159945 --source=tencent  #中证全指能源ETF
    python download_data.py --market=SH --code=561700 --source=tencent  #电力公用事业ETF
    python download_data.py --market=SZ --code=000791 --source=tencent  #甘肃能源
    python download_data.py --market=SH --code=516820 --source=tencent  #医疗创新ETF
    python download_data.py --market=SZ --code=159883 --source=tencent  #医疗器械ETF
    python download_data.py --market=SH --code=600276 --source=tencent  #恒瑞医药-医疗创新
    python download_data.py --market=SZ --code=159887 --source=tencent  #银行ETF
    python download_data.py --market=SH --code=600036 --source=tencent  #招商银行
    python download_data.py --market=SH --code=516190 --source=tencent  #华夏中证文娱传媒ETF
    python download_data.py --market=SZ --code=301551 --source=tencent  #无线传媒
    python download_data.py --market=SZ --code=300017 --source=tencent  #网宿科技
    python download_data.py --market=SH --code=603402 --source=tencent  #陕西旅游
    python download_data.py --market=SH --code=510880 --source=tencent  #华泰柏瑞上证红利ETF
fi

if [ "$type" == "all" -o "$type" == "update" ] ; then
echo "starting update charts ...";
    python candle.py --style=echarts --file=tencent_SH000001.xlsx --code="000001 上证指数"
    python candle.py --style=echarts --file=tencent_SH510050.xlsx --code="510050 华夏上证50ETF"
    python candle.py --style=echarts --file=tencent_SH588000.xlsx --code="588000 科创50ETF"
    python candle.py --style=echarts --file=tencent_SH688981.xlsx --code="688981 中芯国际-科创50"
    python candle.py --style=echarts --file=tencent_SH688256.xlsx --code="688256 寒武纪"
    python candle.py --style=echarts --file=tencent_SH688802.xlsx --code="688802 沐曦股份"
    python candle.py --style=echarts --file=tencent_SH688111.xlsx --code="688111 金山办公"
    python candle.py --style=echarts --file=tencent_SZ159915.xlsx --code="159915 易方达创业板ETF"
    python candle.py --style=echarts --file=tencent_SH516160.xlsx --code="516160 新能源ETF"
    python candle.py --style=echarts --file=tencent_SZ159857.xlsx --code="159857 光伏ETF"
    python candle.py --style=echarts --file=tencent_SZ300102.xlsx --code="300102 乾照光电"
    python candle.py --style=echarts --file=tencent_SH600089.xlsx --code="600089 特变电工-光伏"
    python candle.py --style=echarts --file=tencent_SH512400.xlsx --code="512400 南方中证申万有色金属ETF"
    python candle.py --style=echarts --file=tencent_SZ002460.xlsx --code="002460 赣锋锂业"
    python candle.py --style=echarts --file=tencent_SH600547.xlsx --code="600547 山东黄金"
    python candle.py --style=echarts --file=tencent_SZ000807.xlsx --code="000807 云铝股份"
    python candle.py --style=echarts --file=tencent_SZ002428.xlsx --code="002428 云南锗业"
    python candle.py --style=echarts --file=tencent_SZ159824.xlsx --code="159824 博时新能源汽车ETF"
    python candle.py --style=echarts --file=tencent_SZ002594.xlsx --code="002594 比亚迪"
    python candle.py --style=echarts --file=tencent_SZ159945.xlsx --code="159945 中证全指能源ETF"
    python candle.py --style=echarts --file=tencent_SH561700.xlsx --code="561700 电力公用事业ETF"
    python candle.py --style=echarts --file=tencent_SZ000791.xlsx --code="000791 甘肃能源"
    python candle.py --style=echarts --file=tencent_SH516820.xlsx --code="516820 医疗创新ETF"
    python candle.py --style=echarts --file=tencent_SZ159883.xlsx --code="159883 医疗器械ETF"
    python candle.py --style=echarts --file=tencent_SH600276.xlsx --code="600276 恒瑞医药-医疗创新"
    python candle.py --style=echarts --file=tencent_SZ159887.xlsx --code="159887 银行ETF"
    python candle.py --style=echarts --file=tencent_SH600036.xlsx --code="600036 招商银行"
    python candle.py --style=echarts --file=tencent_SH516190.xlsx --code="516190 华夏中证文娱传媒ETF"
    python candle.py --style=echarts --file=tencent_SZ301551.xlsx --code="301551 无线传媒"
    python candle.py --style=echarts --file=tencent_SZ300017.xlsx --code="300017 网宿科技"
    python candle.py --style=echarts --file=tencent_SH603402.xlsx --code="603402 陕西旅游"
    python candle.py --style=echarts --file=tencent_SH510880.xlsx --code="510880 华泰柏瑞上证红利ETF"
fi