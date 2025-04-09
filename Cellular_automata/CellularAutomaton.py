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
        self.is_river = is_river
        self.lat = lat
        self.lon = lon
        self.stage = stage
        self.value = value
        self.local = [lat, lon]
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
        data_list = []
        for i in range(0,len(self.data),300):
            temp_list = []
            temp_list.append(self.data['S'].values[i])
            temp_list.append(self.data['P'].values[i])
            temp_list.append(self.data['Lon'].values[i])
            temp_list.append(self.data['Lat'].values[i])
            temp_list.append(self.data['is_river'].values[i])
            data_list.append(temp_list)
        k = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                self.grid[i][j] = Cellular(data_list[k][0],data_list[k][1],data_list[k][4],data_list[k][2],data_list[k][3],0,0)
                k += 1
        print(self.grid[0][0].show())
        self.Cellular_dict = {}
    def update(self,fire_cellular:Fire_cellular,fire_points):
        '''
        :param fire_cellular: 火蔓延参数
        :param fire_points: 着火点[[a,b],[c,d]]
        :return:
        '''
        for i in fire_points:
            for j in self.grid:
                for k in self.grid[j]:
                    if self.grid[j][k].local == i:
                        self.grid[j][k].update(fire_cellular)


ca = CellularAutomaton((10,10),'../data/train2.0.csv')