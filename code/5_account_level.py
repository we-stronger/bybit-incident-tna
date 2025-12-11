# -*- coding: utf-8 -*-
import os
import pandas as pd
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import networkx as nx  # 添加 networkx 库用于绘制拓扑图
from graphviz import Digraph


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
            graph[sender].append(receiver)
            receivers.add(receiver)
    return graph, receivers

# 找到根节点（没有作为接收方的账户）
def find_root_nodes(graph, receivers):
    all_senders = set(graph.keys())
    root_nodes = all_senders - receivers
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

# 将层级关系保存为CSV文件
def save_hierarchy_to_csv(hierarchy, output_file):
    rows = []
    for parent, children in hierarchy.items():
        for child in children:
            rows.append([parent, child])
    df = pd.DataFrame(rows, columns=["Parent", "Child"])
    df.to_csv(output_file, index=False)

# 绘制每层的账户个数分布图，并突出显示关键账户
def plot_hierarchy_distribution(hierarchy, key_account_levels, save_path=None):
    level_counts = defaultdict(int)
    key_account_counts = defaultdict(int)
    
    for level_name in hierarchy.keys():
        level_depth = len(level_name.split("."))  # 计算层级深度
        #level_counts[level_depth] += len(hierarchy[level_name]) #这样计算出来的每层账户数量会多
        level_counts[level_depth] += 1 #这样只从头结点考虑，会不会有问题
    
    for level, accounts in key_account_levels.items():
        key_account_counts[level] = len(accounts)
    
    # 转换为DataFrame以便绘图
    levels = sorted(set(level_counts.keys()).union(key_account_counts.keys()))
    total_counts = [level_counts[level] for level in levels]
    key_counts = [key_account_counts.get(level, 0) for level in levels]
    
    df = pd.DataFrame({
        "Level": levels,
        "Total Accounts": total_counts,
        "Key Accounts": key_counts
    })
    
    # 绘制柱状图
    plt.figure(figsize=(12, 6))
    
    bar1 = plt.bar(df["Level"], df["Total Accounts"], color='skyblue', label="Total Accounts")
    bar2 = plt.bar(df["Level"], df["Key Accounts"], color='orange', label="Key Accounts")
    
    plt.xlabel("Level Depth")
    plt.ylabel("Number of Accounts")
    plt.title("Distribution of Accounts by Level Depth (Highlighted Key Accounts)")
    plt.xticks(df["Level"])
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')  # 保存图表
    plt.show()

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
    plt.xlabel("Level Depth")
    plt.ylabel("Number of Key Accounts")
    plt.title("Distribution of Key Accounts by Level Depth")
    plt.xticks(df["Level"])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')  # 保存图表
    plt.show()

# 绘制拓扑结构图，按照层级从左到右绘制
def plot_topology_with_key_accounts(graph, key_accounts):
    G = nx.DiGraph()  # 创建有向图 
    # 只添加关键账户节点及其直接连接的边
    for sender, receivers in graph.items():
        if sender in key_accounts:
            for receiver in receivers:
                if receiver in key_accounts:
                    G.add_edge(sender, receiver) 
    if G.number_of_nodes() == 0 or G.number_of_edges() == 0:
        print("No edges between key accounts to display.")
        return 
    dot_path = r"D:\Graphviz-12.2.1-win64\bin\dot.exe"      # 显式指定 Graphviz 的安装路径
    os.environ["PATH"] += os.pathsep + os.path.dirname(dot_path)  # 添加到系统 PATH 
    dot = Digraph(format='png')         # 使用 graphviz 包生成布局
    dot.attr(rankdir='LR', bgcolor='white')  # 背景颜色设为白色 # 设置 rankdir 属性为 LR (left-to-right)

    # 设置全局节点属性
    dot.attr('node', shape='ellipse', style='filled', fillcolor='lightblue', color='black', fontname='Arial', fontsize='50',fontweight='bold')  # 增大了节点文字大小
    # 设置全局边属性，增加了 penwidth 和箭头大小
    dot.attr('edge', color='gray', arrowhead='vee', arrowsize='3.0', fontname='Arial', fontsize='20', penwidth='5')  # 增加了边的粗细

    # 添加节点，并限制显示的名字长度为前 5 个字符
    for node in G.nodes():
        truncated_name = str(node)[:4]  
        # 对于关键账户使用不同的颜色
        if node in key_accounts:
            dot.node(str(node), label=truncated_name, fillcolor='lightcoral', color='red')
        else:
            dot.node(str(node), label=truncated_name)
    # 添加边
    for u, v in G.edges():
        dot.edge(str(u), str(v))
    # 渲染并显示图形
    output_directory = "D:/BlockchainSpider/data/account_level"  # 指定输出目录为当前工作目录
    try:
        dot.render(filename="topology_graph", directory=output_directory, view=True, engine="dot")
    except Exception as e:
        print(f"Failed to render graph: {e}")

# 绘制关键账户拓扑结构图，使用 NetworkX 自带布局（不依赖 pydot 和 Graphviz）
def plot_topology_with_key_accounts_NetworkX(graph, key_accounts):
    G = nx.DiGraph()  # 创建有向图
    
    # 只添加关键账户节点及其直接连接的边
    for sender, receivers in graph.items():
        if sender in key_accounts:
            for receiver in receivers:
                if receiver in key_accounts:
                    G.add_edge(sender, receiver)
    
    if G.number_of_nodes() == 0:
        print("No edges between key accounts to display.")
        return 
    # 使用 spring_layout 或 kamada_kawai_layout 布局
    pos = nx.spring_layout(G, k=0.5, iterations=50)  # spring_layout 布局
    # pos = nx.kamada_kawai_layout(G)  # 可选：kamada_kawai_layout 布局（更紧凑）

    # 设置节点颜色和大小
    node_colors = ['red' if node in key_accounts else 'skyblue' for node in G.nodes()]
    node_sizes = [300 for _ in G.nodes()]  # 固定节点大小
    plt.figure(figsize=(15, 10))  # 调整图像比例
    ax = plt.gca()  # 获取当前 Axes 对象
    nx.draw(
        G, pos,ax=ax,with_labels=True,node_color=node_colors,node_size=node_sizes,
        font_size=8, font_weight='bold',edge_color='gray',arrows=True
    )
    plt.title("Topology Graph with Key Accounts (Spring Layout)")
    plt.show()

# 将关键账户的层级信息保存为CSV文件
def save_key_account_levels_to_csv(key_account_levels, output_file):
    rows = []
    for level, accounts in key_account_levels.items():
        for account in accounts:
            rows.append([account, level])
    df = pd.DataFrame(rows, columns=["Account", "Level"])
    df.to_csv(output_file, index=False)

# 主函数
if __name__ == "__main__":
    
    transactions, key_accounts = load_transactions(csv_directory)                       # 加载交易数据和关键账户
    graph, receivers = build_graph(transactions)                                        # 构建图结构
    root_nodes = find_root_nodes(graph, receivers)                                      # 找到根节点
    hierarchy, key_account_levels = build_hierarchy(root_nodes, graph, key_accounts)    # 构建层级关系，并标记关键账户
    # 将层级关系保存为CSV文件
    output_csv_file = "D:/BlockchainSpider/data/account_level/hierarchy_output.csv"
    save_hierarchy_to_csv(hierarchy, output_csv_file)
    print(f"Hierarchy saved to {output_csv_file}")
    # 将关键账户的层级信息保存为CSV文件
    key_account_levels_csv_file = "D:/BlockchainSpider/data/account_level/key_account_levels.csv"
    save_key_account_levels_to_csv(key_account_levels, key_account_levels_csv_file)
    print(f"Key account levels saved to {key_account_levels_csv_file}")
    
    # 绘制每层的账户个数分布图，并保存
    #plot_hierarchy_distribution(hierarchy, key_account_levels, save_path="D:/BlockchainSpider/data/account_level/account_distribution.png")
    
    # 单独绘制关键账户的层级分布图，并保存
    #plot_key_account_distribution(key_account_levels, save_path="D:/BlockchainSpider/data/account_level/key_account_distribution.png")
    
    # 绘制拓扑结构图，仅显示关键账户及其直接连接
    plot_topology_with_key_accounts(graph, key_accounts)
