# -*- coding: utf-8 -*-
import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import pickle  # 用于缓存图对象

# Step 1: 合并所有CSV文件
def merge_csv_files(folder_path):
    all_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            all_data.append(df)
    merged_data = pd.concat(all_data, ignore_index=True)
    return merged_data

# Step 2: 构建交易网络图
def build_transaction_graph(data):
    G = nx.DiGraph()  # 创建有向图
    for _, row in data.iterrows():
        sender = row['from']
        receiver = row['to']
        value = row['value']
        # 添加节点和边
        if sender not in G:
            G.add_node(sender)
        if receiver not in G:
            G.add_node(receiver)
        G.add_edge(sender, receiver, weight=value)
    return G

# 缓存图到文件
def save_graph_to_file(G, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(G, f)

# 从文件加载图
def load_graph_from_file(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

# Step 3: 计算复杂网络指标
def calculate_network_metrics(G):
    metrics = {}
    metrics['Number of Nodes'] = G.number_of_nodes()
    metrics['Number of Edges'] = G.number_of_edges()
    metrics['Graph Density'] = nx.density(G)
    metrics['Self-loops'] = len(list(nx.selfloop_edges(G)))
    metrics['Reciprocity'] = nx.reciprocity(G)
    metrics['Clustering Coefficient'] = nx.average_clustering(G)
    # 检查图是否连通
    undirected_G = G.to_undirected()  # 转换为无向图
    if nx.is_connected(undirected_G):
        metrics['Diameter'] = nx.diameter(undirected_G)
        metrics['Average Path Length'] = nx.average_shortest_path_length(undirected_G)   
    else:
        # 如果图不连通，使用最大连通子图
        largest_cc = max(nx.connected_components(undirected_G), key=len)
        largest_subgraph = undirected_G.subgraph(largest_cc)
        metrics['Average Path Length'] = nx.average_shortest_path_length(largest_subgraph)
        metrics['Diameter'] = nx.diameter(largest_subgraph)

    return metrics

# Step 4: 可视化网络图
def visualize_and_save_graph(G, output_file):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)  # 使用弹簧布局
    nx.draw(G, pos, with_labels=False, node_size=10, node_color='skyblue', edge_color='gray', alpha=0.5)
    plt.title("Transaction Network")
    plt.savefig(output_file)
    plt.show()


# 构建gephi输出数据格式
def export_to_gephi(G, output_file):
    nx.write_gexf(G, output_file)


# 假设你已经构建了交易图 G
def export_to_gephi_no_weight(G, output_file):
    # 移除边的权重属性（如果存在）
    G_nw = nx.Graph() if not G.is_directed() else nx.DiGraph()
    G_nw.add_nodes_from(G.nodes())
    G_nw.add_edges_from(G.edges())
    nx.write_gexf(G_nw, output_file)


# 主函数
if __name__ == "__main__":
    # 文件夹路径
    folder_path = "D:/BlockchainSpider/data/Bybit_depth1_new"  # 替换为你的CSV文件夹路径
    #output_image = "transaction_network.png"  # 输出的图片文件名
    graph_cache_path = "D:/BlockchainSpider/data/transaction_graph_cache.pkl"  # 图缓存文件路径

    # Step 1: 合并CSV文件
    print("merge...")
    merged_data = merge_csv_files(folder_path)

    # Step 2: 尝试加载缓存的图，如果不存在则构建新图
    if os.path.exists(graph_cache_path):
        print("Loading transaction graph from cache...")
        transaction_graph = load_graph_from_file(graph_cache_path)
    else:
        print("Building transaction graph...")
        transaction_graph = build_transaction_graph(merged_data)
        save_graph_to_file(transaction_graph, graph_cache_path)

    # Step 3: 计算网络指标
    network_metrics = calculate_network_metrics(transaction_graph)
    print("Network Metrics:")
    for key, value in network_metrics.items():
        print(f"{key}: {value}")
    
    # Step 4: 可视化并保存网络图
    #visualize_and_save_graph(transaction_graph, output_image)

    # 构建gephi输出数据格式
    #print("save gexf...")
    #export_to_gephi(transaction_graph, "D:/BlockchainSpider/data/transaction_network.gexf")
    # 调用函数边没有权重
    #print("save gexf no weight...")
    #export_to_gephi_no_weight(transaction_graph, "D:/BlockchainSpider/data/transaction_network_no_weights.gexf")