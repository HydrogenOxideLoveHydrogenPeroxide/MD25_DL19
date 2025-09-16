# main.py
from DL_dataset import DL19Dataset
from BM25 import BM25Retriever
import ir_measures
import os
from pathlib import Path
from ir_measures import *
from ir_measures import Qrel,ScoredDoc
from argument import args          # ← 引入统一参数

def main():
    # ========== 配置路径 ==========
    collection_path =  args.collection_path

    # ========== 1. 加载数据集 ==========
    ds = DL19Dataset(collection_path)
    ds.load_collection()
    ds.load_queries()
    ds.load_qrels()

    # ========== 2. BM25 检索 ==========
    retriever = BM25Retriever(ds, args)
    retriever.build_index()
    retriever.retrieve()
    retriever.save_run(args.run_save_path)

    # ========== 3. 评测 ==========
    print("[main] Evaluating...")
    qrels_list = [Qrel(qid, did, rel)          # 用 namedtuple 而不是普通 tuple
              for qid, did, rel in ds.qrels]
    run_tuples = []
    for qid, docs_r in retriever.run.items():
        for rank, (docid, score) in enumerate(docs_r, start=1):
            run_tuples.append((qid, docid, rank, score))
    run_list = [ScoredDoc(qid, did, score)
            for qid, did,rank, score in run_tuples]
    measures = [NDCG@10, MRR@10, MAP@1000]
    results  = list(ir_measures.calc(measures, qrels_list, run_list))

    print("[main] BM25 results on DL19:")
    for m in results:
        print(m)

if __name__ == "__main__":
    main()
