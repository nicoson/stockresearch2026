import pandas as pd
import os
from util import config as cf

def load_data(filename=None):
    if filename != None:
        if os.path.exists(filename):
            pd_data = pd.read_excel(filename)
        else:
            pd_data = None
    
    return pd_data

def write_data(pd_data, filename='output.xlsx'):
    # 使用openpyxl作为引擎（默认）
    pd_data.to_excel(filename, sheet_name='Sheet1', index=False, engine='openpyxl')
    print('file saved success !!!')