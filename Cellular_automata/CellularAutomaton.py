import numpy as np
import pandas as pd
from util.WangZhengfei_Model import WangZhengfei_Model

class Fire_cellular:
    def __init__(self,Time,T_max,W_mean,h_min,s,w,p,lat,lon,R):
        '''
        :param Time: 时间
        :param T_max: 日最高气温
        :param W_mean: 中午平均风级
        :param h_min: 日最小相对湿度
        :param s: 可燃物类型
        :param w: 风速
        :param p: 坡度（角度）
        :param lat: 经度
        :param lon: 维度
        :param R: 火蔓延速率
        '''
        self.time = Time
        self.T_max = T_max
        self.W_mean = W_mean
        self.h_min = h_min
        self.s = s
        self.w = w
        self.p = p
        self.lat = lat
        self.lon = lon
        self.R = R

class Cellular:
    def __init__(self,s,p,is_river,lat,lon,stage,value):
        '''
        单个元胞
        :param s: 可燃物类型
        :param p: 坡度
        :param is_river: 是否为河流
        :param lat: 经度
        :param lon: 维度
        :param stage: 元胞状态
        :param value: 元胞值
        '''
        self.s = s
        self.p = p
        self.is_river = (is_river-1).__abs__()
        self.lat = lat
        self.lon = lon
        self.stage = stage
        self.value = value
        self.local = (lat, lon)
        self.x = None
        self.y = None
    def update_value(self,fire_cellular:Fire_cellular):
        self.value = fire_cellular.R * 10
    def show(self):
        return self.s,self.p,self.is_river,self.lat,self.lon,self.stage,self.value,self.local

class CellularAutomaton:
    def __init__(self,grid_size,path):
        '''
        :param grid_size: 沙盘大小,(10,10)
        :param path: 文件路径
        '''
        self.grid_size = grid_size
        self.data = pd.read_csv(path)
        self.grid = np.empty(grid_size,dtype=object)
        self.Cellular_dict = {}
        self.local_dict = {}
        data_list = self.data.iloc[::300, [5, 6, 1, 2, 10]].values

        k = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                self.grid[i][j] = Cellular(data_list[k][0],data_list[k][1],data_list[k][4],data_list[k][2],data_list[k][3],0,0)
                self.Cellular_dict[self.grid[i][j].local] = self.grid[i][j]
                self.local_dict[self.grid[i][j].local] = [i,j]
                k += 1
        self.grid = self.grid.transpose()[::-1]

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                self.Cellular_dict[self.grid[i][j].local] = self.grid[i][j]
                self.local_dict[self.grid[i][j].local] = [i, j]

    def find_Cellular(self,fire_points):
        find_Cellular_dict = {}
        for i in fire_points:
            if self.Cellular_dict[i] is not None:
                find_Cellular_dict[i] = self.Cellular_dict[i]
        return find_Cellular_dict

    def update(self,fire_cellular:Fire_cellular,fire_points):
        '''
        :param fire_cellular: 火蔓延参数
        :param fire_points: 着火点[[a,b],[c,d]]
        :return:
        '''



ca = CellularAutomaton((10,10),'../data/train2.0.csv')
print(ca.find_Cellular([(106.59,26.628),(106.59,26.638)])[(106.59,26.638)].show())
print(ca.local_dict)

