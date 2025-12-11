# -*- coding: utf-8 -*-

import os
import pandas as pd

# 定义一个函数来读取单个文件并提取 contractAddress 和 tokenSymbol 的对应关系
def extract_contract_token_mapping(file_path):
    try:
        # 尝试不同的编码格式读取文件
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(file_path, encoding='utf-16')
            except UnicodeDecodeError:
                try:
                    df = pd.read_csv(file_path, encoding='gbk')
                except UnicodeDecodeError:
                    df = pd.read_csv(file_path, encoding='latin1')

        # 确保 contractAddress 和 tokenSymbol 列存在
        if 'contractAddress' in df.columns and 'tokenSymbol' in df.columns:
            # 提取 contractAddress 和 tokenSymbol 的对应关系
            mapping = df[['contractAddress', 'tokenSymbol']].dropna()  # 去除空值
            return mapping.drop_duplicates()  # 去重后返回
        else:
            print(f"Warning: Missing 'contractAddress' or 'tokenSymbol' column in {file_path}")
            return pd.DataFrame(columns=['contractAddress', 'tokenSymbol'])  # 返回空 DataFrame
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return pd.DataFrame(columns=['contractAddress', 'tokenSymbol'])

# 定义一个函数来处理多个文件
def process_files(directory_path):
    all_mappings = []  # 存储所有文件中的 contractAddress 和 tokenSymbol 的对应关系

    # 遍历目录中的所有 CSV 文件
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.csv'):  # 只处理 CSV 文件
            file_path = os.path.join(directory_path, file_name)
            print(f"Processing file: {file_path}")
            mapping = extract_contract_token_mapping(file_path)
            all_mappings.append(mapping)  # 将当前文件的映射添加到列表中

    # 合并所有文件的映射
    combined_mapping = pd.concat(all_mappings, ignore_index=True)
    unique_mapping = combined_mapping.drop_duplicates()  # 去重
    
    #保存结果
    output_file = "D:/BlockchainSpider/data/decimals.csv"
    unique_mapping.to_csv(output_file, index=False, encoding='utf-8')
    # 输出统计结果
    print(f"\nTotal number of unique contract addresses: {len(unique_mapping['contractAddress'].unique())}")
    print("Unique contract addresses and their corresponding token symbols:")
    for _, row in unique_mapping.iterrows():
        print(f"Contract Address: {row['contractAddress']}, Token Symbol: {row['tokenSymbol']}")

# 主程序入口
if __name__ == "__main__":
    # 指定包含 CSV 文件的目录路径
    directory_path = "D:/BlockchainSpider/data/Bybit_depth1"
    process_files(directory_path)