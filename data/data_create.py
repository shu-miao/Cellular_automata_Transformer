import pandas as pd
import numpy as np
# from util import WangZhengfei_Model
import math

def WangZhengfei_Model(T_max,W_mean,h_min,s,w,p):
    '''
    :param T_max: 日最高气温
    :param W_mean: 中午平均风级
    :param h_min: 日最小相对湿度
    :param s: 可燃物类型
    :param w: 风速
    :param p: 坡度（角度）
    :return: 研究区域可燃物下林火蔓延速率
    '''
    '''
    3	温带针叶林生态区
    4	温带落叶林生态区
    5	热带和亚热带森林生态区
    6	旱生草原生态区
    9	湿地生态区
    10	冻土生态区
    11	北极生态区
    12	亚寒带森林生态区
    13	高山生态区
    14	侵入性物种生态区
    15	其他生态区
    25	城市或人类活动影响区
    26	特殊保护区
    '''
    Ks_dict = {
        '平铺松针': 0.8,
        '枯枝落叶': 1.2,
        '茅草杂草': 1.6,
        '莎草矮桦': 1.8,
        '牧场草原': 2.0,
        '红松、华山松、云南松等林地': 1.0
    }
    Ks = Ks_dict.get(s, 1.0)  # 可燃物综合物理性质与化学性质的燃烧性系数 默认值为1.0
    Ks = 1.0
    Kw_dict = {
        (1, 1): 1.2,
        (1, 2): 1.4,
        (2, 3): 1.7,
        (3, 4): 2.0,
        (4, 5): 2.4,
        (5, 6): 2.9,
        (6, 7): 3.3,
        (7, 8): 4.1,
        (8, 9): 5.1,
        (9, 10): 6.0,
        (10, 11): 7.3,
        (11, 12): 8.5
    }
    Kw = next((value for (lower, upper), value in Kw_dict.items() if lower < w <= upper), 8.5) # # 风速调整系数
    R0 = 0.03 * T_max + 0.05 * W_mean + 0.01 * h_min - 0.3 # 日初始蔓延速率
    p_rad = math.radians(p)  # 转为弧度
    Kp = math.e ** (3.533 * (math.tan(p_rad) ** 1.2))  # 坡度调整系数
    R = R0 * Ks * Kw * Kp # 计算蔓延速率
    return R

def create_R(path):
    data = pd.read_csv(path)
    T_max_list = data['T_max'].values
    W_mean_list = data['W_mean'].values
    H_min_list = data['H_min'].values
    W_list = data['W'].values
    P_list = data['P'].values
    R_list = []
    for i in range(min(3000, len(data))):
        R = WangZhengfei_Model(T_max_list[i],W_mean_list[i],H_min_list[i],'红松、华山松、云南松等林地',W_list[i],P_list[i])
        R_list.append(R)
    data['R'] = pd.Series(R_list, index=data.index[:len(R_list)])
    data.to_csv(path, index=False)
    print(f"已生成{len(R_list)}条R值并保存至{path}")

create_R('train1.0.csv')