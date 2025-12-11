# -*- coding: utf-8 -*-

import pandas as pd
import os

# 数据目录
data_dir = "D:/BlockchainSpider/data/Bybit_depth1_new"

# 获取所有 CSV 文件路径
csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

# 定义一个函数来加载和预处理单个文件
def preprocess_csv(file_path):
    df = pd.read_csv(file_path)
    
    # 时间戳转换
    df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='s')
    
    # 单位转换（假设 value 是以 Wei 为单位）
    # df['value_eth'] = df['value'].astype(float)
    
    # 格式转换
    df['value'] = df['value'].astype(float)
    df['decimals'] = df['decimals'].astype(float)

    # 添加 decimals 列，并根据 decimals 的值计算 value_eth
    df['value_eth'] = df.apply(
        lambda row: row['value'] / (10 ** row['decimals']) if row['decimals'] != 0 else None,
        axis=1
    )
    
    # 删除 decimals 为 0 的记录
    df = df[df['decimals'] != 0]
    
    # 过滤无效交易
    #df = df[df['isError'] == 0]
    
    # 去重
    df.drop_duplicates(inplace=True)
    
    return df

# 创建一个字典存储每个地址的 DataFrame
address_data = {}

for file in csv_files:
    address = file.split(".")[0]  # 提取地址作为键
    file_path = os.path.join(data_dir, file)
    address_data[address] = preprocess_csv(file_path)

# 生命周期分析
lifecycle_results = {}

for address, df in address_data.items():
    if not df.empty:  # 确保数据不为空
        first_txn = df['timeStamp'].min()
        last_txn = df['timeStamp'].max()
        lifecycle_days = (last_txn - first_txn).days
    else:
        first_txn, last_txn, lifecycle_days = None, None, 0
    
    lifecycle_results[address] = {
        'first_txn': first_txn,
        'last_txn': last_txn,
        'lifecycle_days': lifecycle_days
    }

# 转换为 DataFrame
lifecycle_df = pd.DataFrame.from_dict(lifecycle_results, orient='index').reset_index()
lifecycle_df.rename(columns={'index': 'address'}, inplace=True)

# 交易频率分析
txn_freq_results = {}

for address, df in address_data.items():
    if not df.empty:
        total_txns = len(df)
        lifecycle_days = lifecycle_results[address]['lifecycle_days']
        avg_daily_txns = total_txns / lifecycle_days if lifecycle_days > 0 else 0
    else:
        total_txns, avg_daily_txns = 0, 0
    
    txn_freq_results[address] = {
        'total_txns': total_txns,
        'avg_daily_txns': avg_daily_txns
    }

# 转换为 DataFrame
txn_freq_df = pd.DataFrame.from_dict(txn_freq_results, orient='index').reset_index()
txn_freq_df.rename(columns={'index': 'address'}, inplace=True)

# 入度和出度分析
degree_results = {}

for address, df in address_data.items():
    if not df.empty:
        out_degree = df[df['from'] == address].shape[0]
        in_degree = df[df['to'] == address].shape[0]
    else:
        out_degree, in_degree = 0, 0
    
    degree_results[address] = {
        'out_degree': out_degree,
        'in_degree': in_degree
    }

# 转换为 DataFrame
degree_df = pd.DataFrame.from_dict(degree_results, orient='index').reset_index()
degree_df.rename(columns={'index': 'address'}, inplace=True)

# 最终余额分析
balance_results = {}

for address, df in address_data.items():
    if not df.empty:
        total_income = df[df['to'] == address]['value_eth'].sum()
        total_expense = df[df['from'] == address]['value_eth'].sum()
        final_balance = total_income - total_expense
    else:
        total_income, total_expense, final_balance = 0, 0, 0
    
    balance_results[address] = {
        'total_income': total_income,
        'total_expense': total_expense,
        'final_balance': final_balance
    }

# 转换为 DataFrame
balance_df = pd.DataFrame.from_dict(balance_results, orient='index').reset_index()
balance_df.rename(columns={'index': 'address'}, inplace=True)

# 合并所有分析结果

analysis_result = pd.merge(lifecycle_df, txn_freq_df, on='address', how='left')
analysis_result = pd.merge(analysis_result, degree_df, on='address', how='left')
analysis_result = pd.merge(analysis_result, balance_df, on='address', how='left')
# 增加出入度差值
analysis_result['degree_diff'] = analysis_result['in_degree'] - analysis_result['out_degree']

# 查看结果
#print(analysis_result)

# 将最终结果保存为 CSV 文件
output_file = "D:/BlockchainSpider/data/Bybit_depth1_analysis_result_new.csv"
analysis_result.to_csv(output_file, index=False, encoding='utf-8')

#print(f"Analysis result has been saved to {output_file}")


# 可视化部分
import matplotlib.pyplot as plt
import seaborn as sns

# 确保保存目录存在
save_dir = "D:/BlockchainSpider/data/visualizations_new"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 生命周期分布
plt.figure(figsize=(10, 6))
sns.histplot(analysis_result['lifecycle_days'], bins=30, kde=True, color='blue')
plt.title('Distribution of Lifecycle (Days)', fontsize=16)
plt.xlabel('Lifecycle (Days)', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.grid(True)
plt.savefig(os.path.join(save_dir, 'lifecycle_distribution.png'))
plt.show()

# 平均每天交易次数分布
plt.figure(figsize=(10, 6))
sns.histplot(analysis_result['avg_daily_txns'], bins=30, kde=True, color='green')
plt.title('Distribution of Average Daily Transactions', fontsize=16)
plt.xlabel('Average Daily Transactions', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.grid(True)
plt.savefig(os.path.join(save_dir, 'avg_daily_transactions_distribution.png'))
plt.show()


# 入度 vs 出度散点图
plt.figure(figsize=(10, 6))
sns.scatterplot(data=analysis_result, x='in_degree', y='out_degree', color='purple')
plt.title('In-degree vs Out-degree', fontsize=16)
plt.xlabel('In-degree', fontsize=14)
plt.ylabel('Out-degree', fontsize=14)
# 设置 x 轴和 y 轴比例相同
plt.axis('equal')  # 或者使用 scatter_plot.set_aspect('equal')
plt.grid(True)
#plt.savefig(os.path.join(save_dir, 'in_out_degree_scatter.png'))
plt.show()


# 最终余额分布
plt.figure(figsize=(10, 6))
sns.histplot(analysis_result['final_balance'], bins=30, kde=True, color='orange')
plt.title('Distribution of Final Balance (ETH)', fontsize=16)
plt.xlabel('Final Balance (ETH)', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.grid(True)
plt.savefig(os.path.join(save_dir, 'final_balance_distribution.png'))
plt.show()

# 特征相关性热力图
correlation_matrix = analysis_result[['lifecycle_days', 'total_txns', 'avg_daily_txns', 'in_degree', 'out_degree', 'total_income', 'total_expense', 'final_balance']].corr()
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Feature Correlation Heatmap', fontsize=16)
plt.savefig(os.path.join(save_dir, 'feature_correlation_heatmap.png'))
plt.show()

# 按生命周期分组的交易频率箱线图
analysis_result['lifecycle_group'] = pd.cut(analysis_result['lifecycle_days'], bins=[0, 10, 30, 60, 100, float('inf')], labels=['0-10', '11-30', '31-60', '61-100', '>100'])
plt.figure(figsize=(10, 6))
sns.boxplot(data=analysis_result, x='lifecycle_group', y='avg_daily_txns', palette='Set2')
plt.title('Average Daily Transactions by Lifecycle Group', fontsize=16)
plt.xlabel('Lifecycle Group (Days)', fontsize=14)
plt.ylabel('Average Daily Transactions', fontsize=14)
plt.grid(True)
plt.savefig(os.path.join(save_dir, 'avg_daily_transactions_by_lifecycle_group.png'))
plt.show()

# 最终余额 vs 总交易次数散点图
plt.figure(figsize=(10, 6))
sns.scatterplot(data=analysis_result, x='total_txns', y='final_balance', color='red')
plt.title('Final Balance vs Total Transactions', fontsize=16)
plt.xlabel('Total Transactions', fontsize=14)
plt.ylabel('Final Balance (ETH)', fontsize=14)
plt.grid(True)
plt.savefig(os.path.join(save_dir, 'final_balance_vs_total_transactions.png'))
plt.show()
