# -*- coding: utf-8 -*-

import pandas as pd


input_file = 'D:/BlockchainSpider/data/decimals.csv'
output_file = 'D:/BlockchainSpider/data/decimals_processed.csv'

# 读取CSV文件
df = pd.read_csv(input_file)

# 定义一个函数来提取 "uint" 前面的数字，并处理空值
def extract_decimals(value):
    if pd.isna(value) or value.strip() == '':
        return 0  # 如果是空值或空白字符串，返回0
    else:
        # 分割字符串，取 "uint" 前的部分并去除空格
        parts = value.split('uint')
        if len(parts) > 0:
            try:
                return int(parts[0].strip())  # 提取数字部分
            except ValueError:
                return 0  # 如果无法转换为数字，默认返回0
        return 0  # 如果没有找到 "uint"，返回0

# 应用函数到decimals列
df['decimals'] = df['decimals'].apply(extract_decimals)

# 输出处理后的数据到新的CSV文件
df.to_csv(output_file, index=False)

print(f"save file {output_file}")