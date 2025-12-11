# -*- coding: utf-8 -*-
import os
import pandas as pd
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import networkx as nx  # 添加 networkx 库用于绘制拓扑图
from graphviz import Digraph

font_tit=25
font_lab=20

# 所有的CSV文件存储在指定目录下
csv_directory = "D:/BlockchainSpider/data/Bybit_depth1_new"

# 读取所有CSV文件并解析交易数据
def load_transactions(csv_dir):
    transactions = []
    # 使用集合避免重复
    key_accounts = set()  # 存储从文件名中提取的71个账户地址
    for filename in os.listdir(csv_dir):
        if filename.endswith(".csv"):
            # 提取账户地址
            account_address = filename.split(".")[0]
            key_accounts.add(account_address)
            
            file_path = os.path.join(csv_dir, filename)
            df = pd.read_csv(file_path)
            # 提取 'from' 和 'to' 字段
            transactions.extend(df[['from', 'to']].values.tolist())
    return transactions, key_accounts

# 构建图结构
def build_graph(transactions):
    graph = defaultdict(list)  # sender -> [receivers]
    receivers = set()          # 记录所有接收方
    for sender, receiver in transactions:
        if pd.notna(sender) and pd.notna(receiver):  # 确保字段非空
            if receiver in key_accounts and sender in key_accounts :#只保留关键节点的
                graph[sender].append(receiver)
                receivers.add(receiver)
    return graph, receivers

# 找到根节点（没有作为接收方的账户）
def find_root_nodes(graph, receivers):
    all_senders = set(graph.keys())
    root_nodes = all_senders - receivers
    #print(len(all_senders),all_senders)
    #print(len(receivers),receivers)
    #print(root_nodes)
    root_nodes.add('0x47666fab8bd0ac7003bce3f5c3585383f09486e2')#源节点
    return root_nodes

# 构建层级关系，并标记关键账户
def build_hierarchy(root_nodes, graph, key_accounts):
    hierarchy = defaultdict(list)
    visited = set()
    key_account_levels = defaultdict(set)  # 记录关键账户所在的层级
    
    def dfs(node, level_name):
        if node in visited:
            return
        visited.add(node)
        children = graph[node]
        child_level_names = []
        for i, child in enumerate(children):
            child_level_name = f"{level_name}.{i+1}"
            child_level_names.append(child_level_name)
            if child in key_accounts:
                key_account_levels[len(child_level_name.split("."))].add(child)
            dfs(child, child_level_name)
        hierarchy[level_name] = child_level_names
    
    for root in root_nodes:
        if root in key_accounts:
            key_account_levels[1].add(root)  # 根节点如果是关键账户，记录在第一层
        dfs(root, root)
    return hierarchy, key_account_levels

# 单独绘制关键账户的层级分布图
def plot_key_account_distribution(key_account_levels, save_path=None):
    levels = sorted(key_account_levels.keys())
    counts = [len(key_account_levels[level]) for level in levels]
    df = pd.DataFrame({
        "Level": levels,
        "Key Account Count": counts
    })
    # 绘制柱状图
    plt.figure(figsize=(10, 5))
    plt.bar(df["Level"], df["Key Account Count"], color='orange')
    plt.xlabel("Level Depth",fontsize=font_lab)
    plt.ylabel("Number of Key Accounts",fontsize=font_lab)
    #plt.title("Distribution of Key Accounts by Level Depth",fontsize=font_tit)
    plt.xticks(df["Level"])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')  # 保存图表
    plt.show()

# 将关键账户的层级信息保存为 Excel 文件的不同 sheet
def save_key_account_levels_to_excel(key_account_levels, output_file):
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        for level, accounts in key_account_levels.items():
            df = pd.DataFrame(accounts, columns=["Account"])
            sheet_name = f"Level_{level}"
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"Key account levels saved to {output_file}")

# 主函数
if __name__ == "__main__":
    
    transactions, key_accounts = load_transactions(csv_directory)                       # 加载交易数据和关键账户
    graph, receivers = build_graph(transactions)                                        # 构建图结构
    root_nodes = find_root_nodes(graph, receivers)                                      # 找到根节点
    hierarchy, key_account_levels = build_hierarchy(root_nodes, graph, key_accounts)    # 构建层级关系，并标记关键账户

    # 将关键账户的层级信息保存为 Excel 文件的不同 sheet
    key_account_levels_excel_file = "D:/BlockchainSpider/data/account_level_update/key_account_levels.xlsx"
    save_key_account_levels_to_excel(key_account_levels, key_account_levels_excel_file)
    
    # 单独绘制关键账户的层级分布图，并保存
    plot_key_account_distribution(key_account_levels, save_path="D:/BlockchainSpider/Bybit/key_account_distribution.png")