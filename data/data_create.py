import pandas as pd
import numpy as np
from util.WangZhengfei_Model import WangZhengfei_Model
import math

def create_R(path):
    data = pd.read_csv(path)
    T_max_list = data['T_max'].values
    W_mean_list = data['W_mean'].values
    H_min_list = data['H_min'].values
    W_list = data['W'].values
    P_list = data['P'].values
    S_list = data['S'].values
    R_list = []
    for i in range(min(30000, len(data))):
        R = WangZhengfei_Model(T_max_list[i],W_mean_list[i],H_min_list[i],S_list[i],W_list[i],P_list[i])
        R_list.append(R)
    data['R'] = pd.Series(R_list, index=data.index[:len(R_list)])
    data.to_csv(path, index=False)
    print(f"已生成{len(R_list)}条R值并保存至{path}")

create_R('train2.0.csv')