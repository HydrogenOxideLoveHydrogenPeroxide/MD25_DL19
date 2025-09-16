# bm25.py

"""
BM25原理与公式简介
-----------------
BM25（Best Matching 25）是一种基于概率相关模型的文档检索算法，是信息检索领域最常用的文本相关性打分方法之一。BM25的核心思想是：对于给定的查询（Query），根据文档中各个词项的出现情况，计算文档与查询的相关性分数。

BM25的主要公式如下：

    \[
    \text{score}(D, Q) = \sum_{q_i \in Q} IDF(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot (1 - b + b \cdot \frac{|D|}{\text{avgdl}})}
    \]

其中：
- \( Q \)：查询（query），由若干词项 \( q_i \) 组成
- \( D \)：文档
- \( f(q_i, D) \)：词项 \( q_i \) 在文档 \( D \) 中出现的次数
- \( |D| \)：文档 \( D \) 的长度（词数）
- \( \text{avgdl} \)：语料库中文档的平均长度
- \( k_1 \)、\( b \)：可调参数，常用 \( k_1 \in [1.2, 2.0] \)，\( b \in [0.5, 0.8] \)
- \( IDF(q_i) \)：词项 \( q_i \) 的逆文档频率，衡量词项的区分能力

BM25通过对词频、文档长度归一化和逆文档频率的加权，能够有效衡量文档与查询的相关性。

代码实现详解
-----------
"""

from rank_bm25 import BM25Okapi
from collections import defaultdict
from tqdm import tqdm
import numpy as np

class BM25Retriever:
    def __init__(self, dataset, args):
        """
        BM25Retriever初始化函数

        参数:
        - dataset: DL19Dataset 实例，包含文档、查询等信息
        - args   : argument.py 中的 Args 对象，包含BM25参数（k1, b, top_k等）
        """
        self.dataset = dataset
        self.k1      = args.bm25_k1  # BM25参数k1
        self.b       = args.bm25_b   # BM25参数b
        self.top_k   = args.top_k    # 检索返回的top_k文档数
        self.run     = defaultdict(list)  # 检索结果，{qid: [(docid, score), ...]}

    def build_index(self):
        """
        构建BM25索引（即初始化BM25Okapi对象）
        """
        print("[BM25Retriever] Building BM25 index...")
        # rank_bm25 的 BM25Okapi 接收 **k1、b** 参数
        self.bm25 = BM25Okapi(
            self.dataset.corpus,  # 语料库（分词后的文档列表）
            k1=self.k1,
            b=self.b
        )

    def retrieve(self):
        """
        对每个查询进行BM25检索，返回top_k相关文档
        """
        print("[BM25Retriever] Running retrieval...")
        for qid, text in tqdm(self.dataset.queries):
            # 对查询文本分词
            q_tokens = text.lower().split()
            # 计算该查询对所有文档的BM25分数
            scores = self.bm25.get_scores(q_tokens)
            
            # 获取当前query对应的候选文档ID列表
            candidate_doc_ids = self.dataset.query_doc_map[qid]
            
            # 创建doc_id到索引的映射（方便定位文档在self.dataset.doc_ids中的位置）
            doc_id_to_idx = {}
            for i, doc_id in enumerate(self.dataset.doc_ids):
                if doc_id in candidate_doc_ids:
                    doc_id_to_idx[doc_id] = i
            
            # 只对当前query的候选文档进行打分和排序
            candidate_scores = []
            candidate_doc_ids_list = []
            for doc_id in candidate_doc_ids:
                if doc_id in doc_id_to_idx:
                    idx = doc_id_to_idx[doc_id]
                    candidate_scores.append(scores[idx])
                    candidate_doc_ids_list.append(doc_id)
            
            # 对候选文档按分数降序排序，取top_k
            sorted_indices = np.argsort(candidate_scores)[::-1][:self.top_k]
            
            for rank, idx in enumerate(sorted_indices, start=1):
                doc_id = candidate_doc_ids_list[idx]
                score = candidate_scores[idx]
                self.run[qid].append((doc_id, float(score)))

    def save_run(self, path: str):
        """
        保存检索结果到文件，格式为TREC标准run文件
        """
        print(f"[BM25Retriever] Saving run file -> {path}")
        with open(path, "w", encoding="utf8") as f:
            for qid, docs_r in self.run.items():
                for rank, (docid, score) in enumerate(docs_r, start=1):
                    # 写入格式: query_id Q0 doc_id rank score bm25
                    f.write(f"{qid} Q0 {docid} {rank} {score:.6f} bm25\n")