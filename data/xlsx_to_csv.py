import pandas as pd
from datetime import datetime, timedelta


def xlsx_to_csv_with_time(xlsx_file, csv_file):
    """
    将xlsx文件转换为csv文件，并在第一行添加时间列，从2020年1月20日22:30:31开始，每次递增30秒。

    :param xlsx_file: 输入的xlsx文件路径
    :param csv_file: 输出的csv文件路径
    """
    df = pd.read_excel(xlsx_file)

    start_time = datetime(2020, 1, 20, 22, 30, 31)
    time_series = [start_time + timedelta(seconds=60 * i) for i in range(len(df))]

    df.insert(0, 'Time', time_series)

    df.to_csv(csv_file, index=False)


xlsx_to_csv_with_time(r'train1.0.xlsx',
                      r'train1.0.csv')
