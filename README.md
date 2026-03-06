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
