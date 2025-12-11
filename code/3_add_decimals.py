# -*- coding: utf-8 -*-
import pandas as pd
import os

# 读取 decimals.csv 文件
decimals_file = 'D:/BlockchainSpider/data/decimals_processed.csv'
decimals_df = pd.read_csv(decimals_file)

# 创建 contractAddress 到 decimals 的映射
decimals_map = dict(zip(decimals_df['contractAddress'], decimals_df['decimals']))

# 待处理文件夹路径
input_folder = 'D:/BlockchainSpider/data/Bybit_depth1'  # 替换为存放 71 个文件的文件夹路径
output_folder = 'D:/BlockchainSpider/data/Bybit_depth1_process_new'  # 替换为保存更新后文件的文件夹路径

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 遍历待处理文件
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):  # 只处理 CSV 文件
        file_path = os.path.join(input_folder, filename)
        
        # 读取当前文件
        df = pd.read_csv(file_path)
        
        # 添加 decimals 列
        df['decimals'] = df['contractAddress'].map(decimals_map)

        #这里在etherscan上查看了contractAddress为空的交易，是直接转移
        # 如果 contractAddress 为空，则将 decimals 填充为 18
        df['decimals'] = df['decimals'].fillna(18)
        
        # 保存更新后的文件
        output_path = os.path.join(output_folder, filename)
        df.to_csv(output_path, index=False)

print("success")