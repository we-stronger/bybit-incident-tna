# -*- coding: utf-8 -*-
'''
import os
import pandas as pd
from collections import defaultdict

# 设置路径
data_dir = 'D:/BlockchainSpider/data/Bybit_depth1_new'  # 替换为你的实际路径
output_file = 'D:/BlockchainSpider/data/counterparties_with_type.csv'

# 从文件名中提取所有洗钱账户地址
scam_accounts = [
    filename.replace('.csv', '') for filename in os.listdir(data_dir) if filename.endswith('.csv')
]
scam_set = set(addr.lower() for addr in scam_accounts)

# 存储交易对手信息：地址 -> {'internal': count, 'external': count}
counterparty_info = defaultdict(lambda: {'internal': 0, 'external': 0})

# 遍历目录下所有CSV文件
for filename in os.listdir(data_dir):
    if not filename.endswith('.csv'):
        continue

    file_path = os.path.join(data_dir, filename)
    
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        continue

    for _, row in df.iterrows():
        from_addr = row['from'].lower()
        to_addr = row['to'].lower()

        # 判断是否是洗钱账户参与的交易
        from_is_scam = from_addr in scam_set
        to_is_scam = to_addr in scam_set

        if from_is_scam or to_is_scam:
            # 获取交易对手地址
            if from_is_scam:
                counterparty = to_addr
            else:
                counterparty = from_addr

            # 确保交易对手不是空值或非法地址
            if not counterparty.startswith('0x') or len(counterparty) != 42:
                continue

            # 判断交易对手类型
            if counterparty in scam_set:
                counterparty_info[counterparty]['internal'] += 1
            else:
                counterparty_info[counterparty]['external'] += 1

# 构建输出DataFrame
result_list = []
for addr, counts in counterparty_info.items():
    total = counts['internal'] + counts['external']
    label = 'internal' if counts['internal'] > 0 else 'external'
    result_list.append({
        'Counterparty': addr,
        'InternalCount': counts['internal'],
        'ExternalCount': counts['external'],
        'TotalTransactions': total,
        'Type': label
    })

result_df = pd.DataFrame(result_list)
result_df = result_df.sort_values(by='TotalTransactions', ascending=False)

# 保存结果
result_df.to_csv(output_file, index=False)
print(f"? 结果已保存至 {output_file}")

# 可选：输出高频交易对手
high_freq = result_df[result_df['TotalTransactions'] > 5]
print("\n? 高频交易对手（>5次）:")
print(high_freq.head(20))
'''
# -*- coding: utf-8 -*-
import os
import pandas as pd
from collections import defaultdict

# 设置路径
data_dir = 'D:/BlockchainSpider/data/Bybit_depth1_new'  # 存放洗钱账户CSV的目录
output_dir = 'D:/BlockchainSpider/data/counterparty_analysis'  # 输出每个账户的分析结果

# 创建输出目录（如果不存在）
os.makedirs(output_dir, exist_ok=True)

# 提取所有洗钱账户地址
scam_accounts = [
    filename.replace('.csv', '') for filename in os.listdir(data_dir) if filename.endswith('.csv')
]
scam_set = set(addr.lower() for addr in scam_accounts)

# 遍历每个洗钱账户的CSV文件
for filename in os.listdir(data_dir):
    if not filename.endswith('.csv'):
        continue

    # 获取当前洗钱账户地址
    current_scam_account = filename.replace('.csv', '').lower()
    print(f"Analyzing transactions for {current_scam_account}...")

    file_path = os.path.join(data_dir, filename)
    
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        continue

    # 初始化当前账户的交易对手统计
    counterparty_info = defaultdict(lambda: {'internal': 0, 'external': 0})

    # 遍历每条交易记录
    for _, row in df.iterrows():
        from_addr = row['from'].lower()
        to_addr = row['to'].lower()

        # 只关注当前洗钱账户参与的交易
        if from_addr != current_scam_account and to_addr != current_scam_account:
            continue

        # 确定交易对手
        if from_addr == current_scam_account:
            counterparty = to_addr
        else:
            counterparty = from_addr

        # 简单校验地址格式
        if not counterparty.startswith('0x') or len(counterparty) != 42:
            continue

        # 判断交易对手是否是洗钱账户（内部）还是普通账户（外部）
        if counterparty in scam_set:
            counterparty_info[counterparty]['internal'] += 1
        else:
            counterparty_info[counterparty]['external'] += 1

    # 构建DataFrame
    result_list = []
    for addr, counts in counterparty_info.items():
        total = counts['internal'] + counts['external']
        label = 'internal' if counts['internal'] > 0 else 'external'
        result_list.append({
            'Counterparty': addr,
            'InternalCount': counts['internal'],
            'ExternalCount': counts['external'],
            'TotalTransactions': total,
            'Type': label
        })

    result_df = pd.DataFrame(result_list)
    result_df = result_df.sort_values(by='TotalTransactions', ascending=False)

    # 保存结果到 output_dir 下
    output_file = os.path.join(output_dir, f"{current_scam_account}_counterparties.csv")
    result_df.to_csv(output_file, index=False)

print("✅ 所有洗钱账户的交易对手分析已完成。")