# -*- coding: utf-8 -*-

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

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
txn_freq_results = {}
degree_results = {}
balance_results = {}

for address, df in address_data.items():
    if not df.empty:  # 确保数据不为空
        # 生命周期分析
        first_txn = df['timeStamp'].min()
        last_txn = df['timeStamp'].max()
        lifecycle_days = (last_txn - first_txn).days
        
        # 交易频率分析
        total_txns = len(df)
        avg_daily_txns = total_txns / lifecycle_days if lifecycle_days > 0 else 0
        
        # 入度和出度分析
        out_degree = df[df['from'] == address].shape[0]
        in_degree = df[df['to'] == address].shape[0]
        
        # 最终余额分析
        total_income = df[df['to'] == address]['value_eth'].sum()
        total_expense = df[df['from'] == address]['value_eth'].sum()
        final_balance = total_income - total_expense
    else:
        first_txn, last_txn, lifecycle_days = None, None, 0
        total_txns, avg_daily_txns = 0, 0
        out_degree, in_degree = 0, 0
        total_income, total_expense, final_balance = 0, 0, 0
    
    lifecycle_results[address] = {
        'first_txn': first_txn,
        'last_txn': last_txn,
        'lifecycle_days': lifecycle_days
    }
    txn_freq_results[address] = {
        'total_txns': total_txns,
        'avg_daily_txns': avg_daily_txns
    }
    degree_results[address] = {
        'out_degree': out_degree,
        'in_degree': in_degree
    }
    balance_results[address] = {
        'total_income': total_income,
        'total_expense': total_expense,
        'final_balance': final_balance
    }

# 转换为 DataFrame
lifecycle_df = pd.DataFrame.from_dict(lifecycle_results, orient='index').reset_index()
lifecycle_df.rename(columns={'index': 'address'}, inplace=True)

txn_freq_df = pd.DataFrame.from_dict(txn_freq_results, orient='index').reset_index()
txn_freq_df.rename(columns={'index': 'address'}, inplace=True)

degree_df = pd.DataFrame.from_dict(degree_results, orient='index').reset_index()
degree_df.rename(columns={'index': 'address'}, inplace=True)

balance_df = pd.DataFrame.from_dict(balance_results, orient='index').reset_index()
balance_df.rename(columns={'index': 'address'}, inplace=True)

# 合并所有分析结果
analysis_result = pd.merge(lifecycle_df, txn_freq_df, on='address', how='left')
analysis_result = pd.merge(analysis_result, degree_df, on='address', how='left')
analysis_result = pd.merge(analysis_result, balance_df, on='address', how='left')
analysis_result['degree_diff'] = analysis_result['in_degree'] - analysis_result['out_degree']

# 计算总交易金额（总收入 + 总支出）
analysis_result['total_transaction_amount'] = analysis_result['total_income'] + analysis_result['total_expense']
# 计算平均交易金额（总交易金额 / 总交易次数）
analysis_result['average_transaction_amount'] = analysis_result['total_transaction_amount'] / analysis_result['total_txns']
analysis_result['average_transaction_amount'].fillna(0, inplace=True)  # 处理分母为0的情况

# 将最终结果保存为 CSV 文件
#output_file = "D:/BlockchainSpider/data/Bybit_depth1_analysis_result_new.csv"
#analysis_result.to_csv(output_file, index=False, encoding='utf-8')


####################################################################################################

# 可视化部分
label_filt  = True
if label_filt:
    save_dir = "D:/BlockchainSpider/Bybit/individual/filt"
else:
    save_dir = "D:/BlockchainSpider/Bybit/individual/ori"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

if label_filt:
    analysis_result1=analysis_result
    analysis_result2=analysis_result
    analysis_result3=analysis_result[analysis_result['total_txns'] < 4000]
    analysis_result4=analysis_result[analysis_result['in_degree'] <= 3000]
    analysis_result5=analysis_result
    analysis_result6=analysis_result[analysis_result['total_transaction_amount']<0.8*10**10]   
    analysis_result6_1=analysis_result[analysis_result['average_transaction_amount']<2*10**7]           
      
else:
    analysis_result1=analysis_result
    analysis_result2=analysis_result
    analysis_result3=analysis_result
    analysis_result4=analysis_result
    analysis_result5=analysis_result
    analysis_result6=analysis_result
    analysis_result6_1=analysis_result  

###############################################
font_tit=25
font_lab=20

# 1.生命周期分布
plt.figure(figsize=(10, 6))
sns.histplot(analysis_result1['lifecycle_days'], bins=30, kde=False, color='blue')
#plt.title('Distribution of Lifecycle (Days)', fontsize=font_tit)
plt.xlabel('Lifecycle (Days)', fontsize=font_lab)
plt.ylabel('Count', fontsize=font_lab)
plt.grid(True)
plt.savefig(os.path.join(save_dir, 'lifecycle_distribution.png'))
#plt.show()

################################################
# 2.最终余额分布
plt.figure(figsize=(10, 6))
sns.histplot(analysis_result2['final_balance'], bins=30, kde=False, color='orange')
#plt.title('Distribution of Final Balance (ETH)', fontsize=font_tit)
plt.xlabel('Final Balance (ETH)', fontsize=font_lab)
plt.ylabel('Count', fontsize=font_lab)
plt.grid(True)
plt.savefig(os.path.join(save_dir, 'final_balance_distribution.png'))
#plt.show()

##############################################
# 3. 总交易次数直方图

plt.figure(figsize=(10, 6))
sns.histplot(analysis_result3['total_txns'], bins=30, kde=False, color='purple')
#plt.title('Total Transactions Distribution', fontsize=font_tit)
plt.xlabel('Total Transactions', fontsize=font_lab)
plt.ylabel('Count', fontsize=font_lab)
plt.grid(True)
plt.savefig(os.path.join(save_dir, 'total_transactions_distribution.png'))
#plt.show()

# 3.1扇形图
bins = [0, 100, float('inf')]
labels = ['0-100', '>100']
analysis_result['total_txns'] = pd.cut(analysis_result['total_txns'], bins=bins, labels=labels)
txn_counts = analysis_result['total_txns'].value_counts(normalize=True) * 100
plt.figure(figsize=(8, 8))
plt.pie(txn_counts, labels=txn_counts.index, autopct='%1.1f%%', startangle=140)
#plt.title('Total Transactions pie', fontsize=font_tit)
plt.savefig(os.path.join(save_dir, 'total_transactions_distribution_bin.png'))
#plt.show()

##############################################
# 4.出入交易次数：入度 vs 出度散点图
plt.figure(figsize=(10, 6))
scatter_plot = sns.scatterplot(data=analysis_result4, x='in_degree', y='out_degree', color='purple')
#plt.title('In-degree vs Out-degree', fontsize=font_tit)
plt.xlabel('In-degree', fontsize=font_lab)
plt.ylabel('Out-degree', fontsize=font_lab)
# 获取最大值（确保大于等于 0）
max_value = max(analysis_result4['in_degree'].max(), analysis_result4['out_degree'].max())+10
plt.xlim(0, max_value)# 设置 x 轴和 y 轴从 0 开始
plt.ylim(0, max_value)
plt.plot([0, max_value], [0, max_value], color='red', linestyle='--', linewidth=1.5, label='x=y')
plt.grid(True)
plt.legend()
plt.gca().set_aspect('equal', adjustable='box')# 强制设置坐标轴比例一致
plt.savefig(os.path.join(save_dir, 'in_out_degree_scatter.png'))
#plt.show()

##############################################
# 5. 交易频率：关键账户平均每日交易次数的扇形图
bins = [0, 10, 20, 50, float('inf')]
labels = ['0-10', '10-20', '20-50', '>50']
analysis_result['avg_daily_txns_bin'] = pd.cut(analysis_result['avg_daily_txns'], bins=bins, labels=labels)
txn_freq_counts = analysis_result['avg_daily_txns_bin'].value_counts(normalize=True) * 100

plt.figure(figsize=(8, 8))
plt.pie(txn_freq_counts, labels=txn_freq_counts.index, autopct='%1.1f%%', startangle=140)
#plt.title('Average Daily Transactions Distribution', fontsize=font_tit)
plt.savefig(os.path.join(save_dir, 'avg_daily_transactions_pie_chart.png'))
#plt.show()

# 5.1交易频率：平均每天交易次数分布柱状图
plt.figure(figsize=(10, 6))
sns.histplot(analysis_result5['avg_daily_txns'], bins=30, kde=False, color='green')
#plt.title('Distribution of Average Daily Transactions', fontsize=font_tit)
plt.xlabel('Average Daily Transactions', fontsize=font_lab)
plt.ylabel('Count', fontsize=font_lab)
plt.grid(True)
plt.savefig(os.path.join(save_dir, 'avg_daily_transactions_distribution.png'))
#plt.show()

##############################################
# 6.1.总交易金额柱状图
plt.figure(figsize=(12, 6))
sns.histplot(analysis_result6['total_transaction_amount'], bins=30, kde=False, color='blue')
#plt.title('Total Transaction Amount Distribution', fontsize=font_tit)
plt.xlabel('Total Transaction Amount (ETH)', fontsize=font_lab)
plt.ylabel('Number of Accounts', fontsize=font_lab)
plt.grid(True)
plt.savefig(os.path.join(save_dir, 'total_transaction_amount_distribution_filt.png'))
#plt.show()

# 6.2.平均交易金额柱状图

plt.figure(figsize=(12, 6))
sns.histplot(analysis_result6_1['average_transaction_amount'], bins=30, kde=False, color='green')
#plt.title('Average Transaction Amount Distribution', fontsize=font_tit)
plt.xlabel('Average Transaction Amount (ETH)', fontsize=font_lab)
plt.ylabel('Number of Accounts', fontsize=font_lab)
plt.grid(True)
plt.savefig(os.path.join(save_dir, 'average_transaction_amount_distribution_filt.png'))
#plt.show()

# 6.3. 大额交易比例及分布
threshold = analysis_result['total_expense'].quantile(0.9)  # 设定阈值为前10%的交易金额 分位数
large_transactions = analysis_result[analysis_result['total_expense'] >= threshold]
large_transaction_ratio = len(large_transactions) / len(analysis_result) * 100

print(f"Large Transaction Threshold: {threshold:.2f} ETH")
print(f"Percentage of Large Transactions: {large_transaction_ratio:.2f}%")

plt.figure(figsize=(8, 8))
plt.pie([large_transaction_ratio, 100 - large_transaction_ratio], 
        labels=['Large Transactions', 'Small Transactions'], 
        autopct='%1.1f%%', startangle=140)
#plt.title('Large vs Small Transactions', fontsize=font_tit)
plt.savefig(os.path.join(save_dir, 'large_vs_Small_transactions_pie_chart_expense.png'))
#plt.show()

if False:   #这些是筛选出来的账户的地址

    filtered_result = analysis_result[analysis_result['total_txns'] >= 4000]
    print("total_txns:\n",filtered_result['address'])

    filtered_result = analysis_result[analysis_result['in_degree'] > 3000]
    print("in_degree:\n",filtered_result['address'])

    filtered_result = analysis_result[analysis_result['total_transaction_amount']>=0.8*10**10]
    print("total_transaction_amount:\n",filtered_result['address'])

    filtered_result = analysis_result[analysis_result['average_transaction_amount']>=2*10**7]
    print("average_transaction_amount:\n",filtered_result['address'])


