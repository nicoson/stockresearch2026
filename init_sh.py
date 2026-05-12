import os

watchlist = [(dict(catagory = '大盘指数',
        list = [
            ['SH', '000001', '上证指数'],
            ['SH', '510050', '华夏上证50ETF'],
        ])),
    (dict(catagory = '科创板块',
        list = [
            ['SH', '588000', '科创50ETF'],
            ['SH', '688981', '中芯国际-科创50'],
            ['SH', '688256', '寒武纪'],
            ['SH', '688802', '沐曦股份'],
            ['SH', '688111', '金山办公'],
        ])),
    (dict(catagory = '芯片、算力、光模块',
        list = [
            ['SZ', '000988', '华工科技'],
            ['SZ', '002281', '光迅科技'],
            ['SZ', '002428', '云南锗业'],
        ])),
    (dict(catagory = '创业板',
        list = [
            ['SZ', '159915', '易方达创业板ETF'],
        ]
    )),
    (dict(catagory = '新能源、光伏板块',
        list = [
            ['SH', '516160', '新能源ETF'],
            ['SZ', '159857', '光伏ETF'],
            ['SZ', '300102', '乾照光电'],
            ['SH', '600089', '特变电工-光伏'],
        ]
    )),
    (dict(catagory = '有色金属',
        list = [
            ['SH', '512400', '南方中证申万有色金属ETF'],
            ['SZ', '002460', '赣锋锂业'],
            ['SH', '600547', '山东黄金'],
            ['SZ', '000807', '云铝股份'],
        ]
    )),
    (dict(catagory = '新能源汽车',
        list = [
            ['SZ', '159824', '博时新能源汽车ETF'],
            ['SZ', '002594', '比亚迪'],
        ]
    )),
    (dict(catagory = '能源、电力',
        list = [
            ['SZ', '159945', '中证全指能源ETF'],
            ['SH', '561700', '电力公用事业ETF'],
            ['SZ', '000791', '甘肃能源'],
        ]
    )),
    (dict(catagory = '医疗板块',
        list = [
            ['SH', '516820', '医疗创新ETF'],
            ['SZ', '159883', '医疗器械ETF'],
            ['SH', '600276', '恒瑞医药-医疗创新'],
        ]
    )),
    (dict(catagory = '金融板块',
        list = [
            ['SZ', '159887', '银行ETF'],
            ['SH', '600036', '招商银行'],
        ]
    )),
    (dict(catagory = '传媒娱乐',
        list = [
            ['SH', '516190', '华夏中证文娱传媒ETF'],
            ['SZ', '301551', '无线传媒'],
        ]
    )),
    (dict(catagory = '其他',
        list = [
            ['SZ', '300017', '网宿科技'],
            ['SH', '603402', '陕西旅游'],
            ['SH', '510880', '华泰柏瑞上证红利ETF'],
        ]
    )),
    ]

print(watchlist)

# 创建/更新 exec.sh
with open('exec.sh', 'w') as file:
    temp = '''#!/bin/bash
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
    python download_data.py --source=SSE_RZRQ  #上证融资融券数据
'''
    
    for item in watchlist:
        for stock in item['list']:
            temp = temp + '    python download_data.py --market={0} --code={1} --source=tencent  #{2}\n'.format(*stock)

    temp = temp + '''fi\n
if [ "$type" == "all" -o "$type" == "update" ] ; then
echo "starting update charts ...";
'''

    for item in watchlist:
        for stock in item['list']:
            temp = temp + '    python candle.py --style=echarts --file=tencent_{0}{1}.xlsx --code="{1} {2}" --file2=tencent_SH000001.xlsx --code2="000001 上证指数"\n'.format(*stock)

    temp = temp + 'fi'

    # print(temp)
    file.write(temp)


# 创建/更新 stocklist.js
with open('imgs/stocklist.js', 'w') as file:
    temp = 'let stock = ['

    for item in watchlist:
        temp = temp + '{' + '''
        catagory: '{0}',
        list: ['''.format(item['catagory'])
        
        for stock in item['list']:
            temp = temp + '"{1} {2}",'.format(*stock)
    
        temp = temp + ']\n    },'
    
    temp = temp + ']'
    # print(temp)
    file.write(temp)