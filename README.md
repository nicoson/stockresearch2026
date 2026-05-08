## 文件说明
download_data.py    下载开源数据
candle.py           绘制k线图
tushare.js          nodejs http方式请求tushare数据

## conda 环境配置说明
* 创建环境：conda create --name my_env python=3.8
* 激活环境‌：conda activate env_name
* ‌查看环境‌：conda env list 或 conda info --envs
* ‌关闭环境‌：conda deactivate
* ‌删除环境‌：conda env remove --name env_name
* 添加清华源：conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
* 源查询：conda config --show channels


## vscode 配置说明
.vscode/launch.json: 需要配置conda环境的地址  
地址获取方法：  

```shell
> conda activate stockresearch
> which python
```

## 初始化执行
在文件 *init_sh.py* 中配置股票代码清单，并执行如下命令：

```shell
> python init_sh.py
```

以上初始化命令将生成初始执行文件
* exec.sh：用以执行下载/更新图表程序；
* ./imgs/stocklist.js：用以执行dashboard.htm的代码配置文件

## 更新股票列表
通初始化执行一致，当修改了股票代码清单后，需要再次执行初始化命令，用以更新执行程序的配置文件

## 更新图表
执行如下命令，可更新股票分析网页：

```shell
> sh exec.sh -n all
```

如果无需更新数据，仅更新图表，则执行如下命令：

```shell
> sh exec.sh -n update
```

## 图表展示
在浏览器中打开如下目录中的文件即可：
./imgs/dashboard.htm