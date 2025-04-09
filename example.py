import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim


# 定义位置编码函数
def positional_encoding(lat, lon, d_model):
    """
    将经纬度转换为位置编码
    :param lat: 纬度
    :param lon: 经度
    :param d_model: 模型维度
    :return: 位置编码
    """
    # 归一化经纬度
    lat = (lat + 90) / 180  # 将纬度转换到[0, 1]范围
    lon = (lon + 180) / 360  # 将经度转换到[0, 1]范围

    # 生成位置编码
    position = np.zeros((1, d_model))
    for pos in range(d_model // 2):
        # 计算经缩放因子变换后的经纬度的正余弦值
        position[0, 2 * pos] = np.sin(lat * (2 * np.pi) * (1 / (10000 ** (2 * pos / d_model))))
        position[0, 2 * pos + 1] = np.cos(lat * (2 * np.pi) * (1 / (10000 ** (2 * pos / d_model))))
        position[0, 2 * pos] += np.sin(lon * (2 * np.pi) * (1 / (10000 ** (2 * pos / d_model))))
        position[0, 2 * pos + 1] += np.cos(lon * (2 * np.pi) * (1 / (10000 ** (2 * pos / d_model))))

    return torch.tensor(position, dtype=torch.float32)

class TimeSeriesTransformer(nn.Module):
    def __init__(self,d_model,n_heads,num_layers):
        super(TimeSeriesTransformer,self).__init__()
        self.encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=d_model,nhead=n_heads),
            num_layers=num_layers
        )
        self.fc = nn.Linear(d_model,1)

    def forward(self,x):
        x = self.encoder(x)
        return self.fc(x[-1])

class CellularAutomaton:
    def __init__(self,grid_size):
        self.grid_size = grid_size
        self.grid = np.zeros((grid_size,grid_size))

    def update(self,speed):
        '''
        更新元胞状态
        :param speed: 速度值
        :return:
        '''
        self.grid += speed.item()

def main():
    data_file = 'data/train2.csv'
    data = pd.read_csv(data_file,nrows=1000)

    latitudes = data['lat'].values
    longitudes = data['lon'].values
    features = data[['tmax','ws','Biomass','dem','slope']].values
    targe = data['aspect']

    d_model = 7
    inputs = []
    for lat,lon,*feature in zip(latitudes,longitudes,*features.T):
        pos_enc = positional_encoding(lat,lon, d_model)
        feature_tensor = torch.tensor(feature,dtype=torch.float32)
        combined_input = torch.cat((pos_enc.squeeze(0),feature_tensor),dim=0)
        inputs.append(combined_input)
    inputs = torch.stack(inputs).unsqueeze(1)

    model = TimeSeriesTransformer(d_model=d_model + 5,n_heads=4,num_layers=2)
    optimizer = optim.Adam(model.parameters(),lr=0.001)
    criterion = nn.MSELoss()

    for epoch in range(100):
        model.train()
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs,torch.tensor(targe,dtype=torch.float32).unsqueeze(1))
        loss.backward()
        optimizer.step()
        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch + 1}/100], Loss:{loss.item():.4f}')

    model.eval()
    predicted_targe = model(inputs[-1].unsqueeze(0))

    ca = CellularAutomaton(grid_size=10)
    ca.update(predicted_targe)

    print(ca.grid)

if __name__ == "__main__":
    main()