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
    ds.load_collection()  # 现在load_collection已经包含了queries的加载
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

    # 写入参数和评测结果到README.md
    readme_path = "README.md"
    bm25_k1 = args.bm25_k1
    bm25_b = args.bm25_b
    top_k = args.top_k

    # 提取指标结果
    result_dict = results[0]
    rr10 = result_dict.get(MRR@10, 0.0)
    ap1000 = result_dict.get(MAP@1000, 0.0)
    ndcg10 = result_dict.get(NDCG@10, 0.0)

    # 追加写入README.md
    with open(readme_path, "a", encoding="utf-8") as f:
        f.write(f"| {bm25_k1} | {bm25_b} | {top_k} | {rr10:.4f} | {ap1000:.4f} | {ndcg10:.4f} |\n")

if __name__ == "__main__":
    main()
