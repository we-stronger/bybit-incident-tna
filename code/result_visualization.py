# 可视化部分
import matplotlib.pyplot as plt
import seaborn as sns

# 确保保存目录存在
save_dir = "D:/BlockchainSpider/data/visualizations"
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
plt.grid(True)
plt.savefig(os.path.join(save_dir, 'in_out_degree_scatter.png'))
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