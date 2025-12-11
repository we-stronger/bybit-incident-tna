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

The dataset focuses on the Bybit Exploit incident and associated money laundering activities.

* **Data Source**: Labeled `Bybit Exploit` accounts from Etherscan and their related transaction records.
* **Network Scale**:
    * **Nodes**: 11,340 (Accounts including hackers and normal addresses)
    * **Edges**: 14,416 (Directed Transactions)
* **Attributes**: Transaction hash, block timestamp, sender, receiver, value (ETH), etc.

## 🧪 Key Findings

Based on the empirical analysis of this dataset, the paper highlights the following patterns in money laundering accounts:

* **Short Lifecycle**: The average lifecycle of money laundering accounts is only **7.75 days**, indicating their disposable nature.
* **High Frequency**: **83.3%** of these accounts conduct more than 10 transactions per day, with distinct bursts of activity to disperse funds rapidly.
* **Flow Patterns (The 3 Stages)**:
    * **Placement**: Accounts show high In-degree (receiving dispersed funds).
    * **Layering**: Accounts show high In-degree & Out-degree (complex mixing behaviors).
    * **Integration**: Accounts show high Out-degree (flowing funds to CEX, DEX, or Stablecoins).
* **Network Topology**: The network exhibits high density (**0.000112**) and low reciprocity (**0.0146**), indicating that funds flow unidirectionally to obscure origins and minimize tracking risks.
