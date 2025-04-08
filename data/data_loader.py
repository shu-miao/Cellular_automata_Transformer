import pandas as pd
from torch.utils.data import DataLoader,Dataset
import os
from sklearn.preprocessing import StandardScaler
import numpy as np

class FireDataset(Dataset):
    def __init__(self,path,numeric_cols,time_code=None,local_code=None):
        '''
        :param path: 文件路径
        :param numeric_cols: 数值特征项['tmax','ws','Biomass','dem','slope','aspect']
        :param time_code: 时间编码方式
        :param local_code: 地理位置（经纬度）编码方式
        '''
        self.dataset = pd.read_csv(path)
        self.time_code = time_code
        self.local_code = local_code
        self.dataset.ffill(inplace=True)
        self.numeric_cols = numeric_cols
        # ['tmax','ws','Biomass','dem','slope','aspect']
        for col in numeric_cols:
            self.dataset[col] = pd.to_numeric(self.dataset[col],errors='coerce')

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, item):
        item = self.dataset[item]