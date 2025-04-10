import numpy as np
import pandas as pd

class Fire_cellular:
    def __init__(self, Time, T_max, W_mean, h_min, s, w, p, lat, lon, R):
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
    def __init__(self, s, p, is_river, lat, lon, stage, value):
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
        self.local = (lat, lon)

    def update_value(self, fire_cellular: Fire_cellular):
        self.value += fire_cellular.R * 1 * (self.is_river - 1).__abs__()
        if self.value >= 255:
            self.value = 255

    def show(self):
        return self.s, self.p, self.is_river, self.lat, self.lon, self.stage, self.value, self.local

class CellularAutomaton:
    def __init__(self, grid_size, path):
        '''
        :param grid_size: 沙盘大小,(10,10)
        :param path: 文件路径
        '''
        self.grid_size = grid_size
        self.data = pd.read_csv(path)
        self.grid = np.empty(grid_size, dtype=object)
        self.Cellular_dict = {}
        self.local_dict = {}
        data_list = self.data.iloc[::300, [5, 6, 1, 2, 10]].values
        k = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                self.grid[i][j] = Cellular(data_list[k][0], data_list[k][1], data_list[k][4], data_list[k][2], data_list[k][3], 0, 0)
                self.Cellular_dict[self.grid[i][j].local] = self.grid[i][j]
                self.local_dict[self.grid[i][j].local] = [i, j]
                k += 1
        self.grid = self.grid.transpose()[::-1]

    def find_Cellular(self, fire_points):
        find_Cellular_dict = {}
        for i in fire_points:
            if i in self.Cellular_dict:
                find_Cellular_dict[i] = self.Cellular_dict[i]
        return find_Cellular_dict

    def get_neighbours(self, fire_point):
        center = self.local_dict[fire_point]
        neighbours_dict = {}
        directions = [
            (-1, 0), (1, 0),  # 上下
            (0, -1), (0, 1),  # 左右
            (-1, -1), (1, 1),  # 左上、右下
            (-1, 1), (1, -1)  # 右上、左下
        ]

        for dx, dy in directions:
            new_x, new_y = center[0] + dx, center[1] + dy
            if 0 <= new_x < self.grid_size[0] and 0 <= new_y < self.grid_size[1]:  # 确保在边界内
                neighbours_dict[(new_x, new_y)] = self.grid[new_x][new_y]

        return neighbours_dict

    def update(self, fire_cellular: Fire_cellular, fire_points):
        '''
        :param fire_cellular: 火蔓延参数
        :param fire_points: 着火点[(106.59,26.628),(106.59,26.638)]
        '''
        changed = True
        history = []

        # 初始化着火元胞
        for point in fire_points:
            if point in self.Cellular_dict:
                self.Cellular_dict[point].value = 100  # 设置初始值为100

        neighbour_values_list = []
        neighbour_values_list_temp = []
        while changed:
            changed = False
            current_state = {}

            # 更新元胞状态
            for point in fire_points:
                if point in self.Cellular_dict:
                    cell = self.Cellular_dict[point]
                    cell.update_value(fire_cellular)
                    # 记录状态变化
                    current_state[point] = cell.value
                    if cell.value != 255:
                        changed = True
                    # print(current_state)
                    if cell.value > 100:
                        neighbours = self.get_neighbours(point)
                        for neighbour_point, neighbour_cell in neighbours.items():
                            if neighbour_point not in fire_points:
                                fire_points.append(neighbour_point)
                            neighbour_cell.update_value(fire_cellular)
                            current_state[neighbour_point] = neighbour_cell.value
                            if neighbour_cell.value not in neighbour_values_list:
                                neighbour_values_list.append(neighbour_cell.value)
                            if neighbour_values_list_temp != neighbour_values_list:
                                neighbour_values_list_temp = neighbour_values_list
                                changed = True

            # 保存当前状态
            if current_state:
                history.append({(cell.lat, cell.lon): value for (point, value) in current_state.items()})

            # 更新火点
            # fire_points = list(current_state.keys())
            print(history)
        return history



ca = CellularAutomaton((10,10),'../data/train2.0.csv')
fire_cellular = Fire_cellular('2025/4/8 12:01:00',11.01,29.41807,85.9576,1.8,15.91482,0.92295,26.628,106.59,37.031)
history = ca.update(fire_cellular,[(106.59,26.638)])
print(len(history),history)
# print(ca.find_Cellular([(106.59,26.628),(106.59,26.638)])[(106.59,26.638)].show())
# print(ca.local_dict)

