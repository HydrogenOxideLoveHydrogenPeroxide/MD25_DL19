# bm25.py
from rank_bm25 import BM25Okapi
from collections import defaultdict
from tqdm import tqdm
import numpy as np

class BM25Retriever:
    def __init__(self, dataset, args):
        """
        dataset: DL19Dataset 实例
        args   : argument.py 中的 Args 对象
        """
        self.dataset = dataset
        self.k1      = args.bm25_k1
        self.b        = args.bm25_b
        self.top_k   = args.top_k
        self.run     = defaultdict(list)  # {qid: [(docid, score), ...]}

    def build_index(self):
        print("[BM25Retriever] Building BM25 index...")
        # rank_bm25 的 BM25Okapi 接收 **k1、b** 参数
        self.bm25 = BM25Okapi(
            self.dataset.corpus,
            k1=self.k1,
            b=self.b
        )

    def retrieve(self):
        print("[BM25Retriever] Running retrieval...")
        for qid, text in tqdm(self.dataset.queries):
            q_tokens = text.lower().split()
            scores = self.bm25.get_scores(q_tokens)
            top_idx = np.argsort(scores)[::-1][:self.top_k]
            for rank, idx in enumerate(top_idx, start=1):
                self.run[qid].append(
                    (self.dataset.doc_ids[idx], float(scores[idx]))
                )

    def save_run(self, path: str):
        print(f"[BM25Retriever] Saving run file -> {path}")
        with open(path, "w", encoding="utf8") as f:
            for qid, docs_r in self.run.items():
                for rank, (docid, score) in enumerate(docs_r, start=1):
                    f.write(f"{qid} Q0 {docid} {rank} {score:.6f} bm25\n")