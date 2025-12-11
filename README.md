# bybit-incident-tna

This repository contains the dataset and source code for the paper **"Understanding Ethereum Money Laundering via Transaction Network Analysis: A Case Study of the Bybit Incident"** (2025).

**Authors:** Yanli Ding, Dan Lin, Weipeng Zou, Bozhao Zhang, Jun Wang, Ting Chen, Letian Sha, and Jiajing Wu.

---

## 📖 Abstract

The anonymity and decentralization features of cryptocurrencies have facilitated complex on-chain money laundering activities. This project analyzes the **Bybit attack (February 2025)**, where hackers exploited a multi-signature vulnerability to steal approximately **$1.4 billion worth of ETH**.

We construct a multidimensional framework utilizing labeled data, transaction network structures, and cross-chain path analysis to investigate money laundering behaviors on the Ethereum network. Through graph model analysis of a large-scale network (**11,000+ nodes and 14,000+ edges**), we systematically dissect money laundering strategies across individual, local, and global dimensions.

## 🚀 Key Features of the Framework

The empirical analysis framework is divided into three main stages:

1.  **Input:** Data collection of labeled accounts and transaction records (leveraging tools like [BlockChainSpider](https://github.com/wuzhy1ng/BlockchainSpider)).
2.  **Multi-dimensional Analysis:**
    * **Individual Level:** Analysis of account lifecycles, transaction frequencies, and balances.
    * **Local Level:** Identification of the three stages of money laundering (Placement, Layering, Integration) based on degree topology.
    * **Global Level:** Network metrics analysis including Reciprocity, Graph Density, and Path Length.
3.  **Output:** Characterization of money laundering behavioral patterns and strategies.
## 📊 Dataset Description

[cite_start]The dataset focuses on the Bybit Exploit incident and associated money laundering activities[cite: 78, 81].

* [cite_start]**Data Source**: Labeled `Bybit Exploit` accounts from the blockchain explorer Etherscan [cite: 69, 86] [cite_start]and their related transaction records[cite: 71].
* **Network Scale**:
    * [cite_start]**Nodes**: 11,340 (Accounts including money laundering and normal accounts)[cite: 78].
    * [cite_start]**Edges**: 14,416 (Directed Transactions)[cite: 78].
* [cite_start]**Attributes**: Transaction timestamps, transaction amounts (converted to ETH), etc.[cite: 73, 77].

## 🧪 Key Findings

Based on the empirical analysis of this dataset, the paper highlights the following patterns in money laundering accounts:

* [cite_start]**Short Lifecycle**: The average lifecycle of money laundering accounts is only **7.75 days** [cite: 94][cite_start], indicating their disposable nature[cite: 95].
* [cite_start]**High Frequency**: **83.3%** of these accounts conduct more than 10 transactions per day [cite: 138][cite_start], often displaying bursts of trading activities within a short period[cite: 140, 145].
* [cite_start]**Flow Patterns (The 3 Stages)**: Accounts are categorized based on their topological relationships[cite: 160, 164].
    * [cite_start]**Placement**: Accounts in the first layer tend to exhibit higher **In-degree** due to receiving numerous small deposits[cite: 164, 170, 172].
    * [cite_start]**Layering**: Accounts (layers 2 to 10) exhibit high **In-degree & Out-degree** with complex and varied transaction patterns[cite: 164, 175, 184].
    * [cite_start]**Integration**: Accounts (layers 11 to 17) often show higher **Out-degree** as funds are transferred to final destinations like centralized exchanges (CEX), decentralized exchanges (DEX), or Stablecoins[cite: 164, 190, 197, 202].
* [cite_start]**Network Topology**: The network exhibits high density (**0.000112**) [cite: 210] [cite_start]compared to normal networks ($10^{-7}$ order) [cite: 210] [cite_start]and low reciprocity (**0.0146**) [cite: 212][cite_start], indicating that funds flow unidirectionally to obscure origins and minimize tracking risks[cite: 213, 214].

