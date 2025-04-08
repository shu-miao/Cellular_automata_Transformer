import numpy as np
import pandas as pd
from util.WangZhengfei_Model import WangZhengfei_Model

class Fire_cellular:
    def __init__(self,T_max,W_mean,h_min,s,w,p,lat,lon):
        '''
        :param T_max: 日最高气温
        :param W_mean: 中午平均风级
        :param h_min: 日最小相对湿度
        :param s: 可燃物类型
        :param w: 风速
        :param p: 坡度（角度）
        :param lat: 经度
        :param lon: 维度
        '''
        self.T_max = T_max
        self.W_mean = W_mean
        self.h_min = h_min
        self.s = s
        self.w = w
        self.p = p
        self.lat = lat
        self.lon = lon

class CellularAutomaton:
    def __init__(self,grid_size,granularity):
        '''
        :param grid_size: 沙盘大小
        :param granularity: 经纬度粒度
        '''
        self.grid_size = grid_size
        self.granularity = granularity
        self.grid = np.zeros((grid_size, grid_size))
        self.Cellular_dict = {}
    def update(self,fire_cellular:Fire_cellular):
        '''
        :param fire_cellular: 火蔓延参数
        :return:
        '''
        self.Cellular_dict[self.grid[self.grid_size * 0.5, self.grid_size * 0.5]] = fire_cellular # 添加初始位置到沙盘中心
