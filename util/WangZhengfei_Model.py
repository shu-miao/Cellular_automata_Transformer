import numpy
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
    Ks_dict = {
        '平铺松针': 0.8,
        '枯枝落叶': 1.2,
        '茅草杂草': 1.6,
        '莎草矮桦': 1.8,
        '牧场草原': 2.0,
        '红松、华山松、云南松等林地': 1.0
    }
    Ks = Ks_dict.get(s, 1.0)  # 可燃物综合物理性质与化学性质的燃烧性系数 默认值为1.0
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

class WangZhengfeiModel:
    def __init__(self,T,W,h):
        '''
        :param T: 日最高气温
        :param W: 中午平均风级
        :param h: 日最小相对湿度
        '''
        self.T = T
        self.W = W
        self.h = h
        # a,b,c,D为常数
        self.a = 0.03
        self.b = 0.05
        self.c = 0.01
        self.D = 0.3

    def get_R(self, s, w, p):
        '''
        :param s: 可燃物类型
        :param w: 风速
        :param p: 坡度（角度）
        :return: R 研究区域可燃物下林火蔓延速率
        '''

        Ks_dict = {
            '平铺松针': 0.8,
            '枯枝落叶': 1.2,
            '茅草杂草': 1.6,
            '莎草矮桦': 1.8,
            '牧场草原': 2.0,
            '红松、华山松、云南松等林地': 1.0
        }

        self.Ks = Ks_dict.get(s, 1.0)  # 可燃物综合物理性质与化学性质的燃烧性系数 默认值为1.0

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
        self.Kw = next((value for (lower, upper), value in Kw_dict.items() if lower < w <= upper), 8.5) # # 风速调整系数

        self.R0 = self.a * self.T + self.b * self.W + self.c * self.h - self.D # # 日初始蔓延速率
        p_rad = math.radians(p)  # 转为弧度
        self.Kp = math.e ** (3.533 * (math.tan(p_rad) ** 1.2)) # 坡度调整系数
        self.R = self.R0 * self.Ks * self.Kw * self.Kp # 计算蔓延速率

        return self.R