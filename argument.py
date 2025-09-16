# argument.py
from dataclasses import dataclass
from pathlib import Path
import os
@dataclass
class Args:
    # 路径
    collection_path : str = Path(os.getcwd())/"corpus/msmarco-passagetest2019-top1000.tsv"
    run_save_path   : str = "bm25.run"

    # BM25 参数
    bm25_k1 : float = 0.3
    bm25_b  : float = 0.7
    top_k   : int   = 100

# 全局单例
args = Args()