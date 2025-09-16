# dataset.py
import csv,os
from pathlib import Path
import ir_datasets
from argument import args   

class DL19Dataset:
    def __init__(self, collection_path):
        """
        collection_path: collection.tsv
        queries_path: DL19的queries文件（不再使用，直接用irdatasets加载）
        qrels_path: qrels.trec_dl_2019.txt（不再使用，直接用irdatasets加载）
        """
        self.collection_path = collection_path

        self.doc_ids = []
        self.corpus = []
        self.queries = []
        self.qrels = []

    def load_collection(self):
        """
        读取msmarco-passagetest2019-top1000.tsv格式的文件
        格式：query_id \t doc_id \t query_text \t document_text
        这里针对特定的query_id和query_text，提取前1000名候选文档，后续用BM25对这些候选文档重新排序并评测。
        """
        print("[DL19Dataset] Loading collection from msmarco-passagetest2019-top1000.tsv...")
        self.doc_ids = []
        self.corpus = []
        self.queries = []
        self.query_doc_map = {}  # {query_id: [doc_id1, doc_id2, ...]}
        self.query_text_map = {} # {query_id: query_text}

        with open(self.collection_path, 'r', encoding='utf8') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if len(row) >= 4:
                    query_id, doc_id, query_text, document_text = row[0], row[1], row[2], row[3]
                    # 记录query_id和query_text（只保留第一个出现的query_text）
                    if query_id not in self.query_text_map:
                        self.query_text_map[query_id] = query_text
                        self.queries.append((query_id, query_text))
                    # 记录每个query_id对应的doc_id列表
                    if query_id not in self.query_doc_map:
                        self.query_doc_map[query_id] = []
                    self.query_doc_map[query_id].append(doc_id)
                    # 记录文档
                    self.doc_ids.append(doc_id)
                    self.corpus.append(document_text.lower().split())

        print(f"Loaded {len(self.corpus)} query-doc pairs from {self.collection_path}")
        print(f"Loaded {len(self.queries)} unique queries from {self.collection_path}")

    def load_queries(self):
        print("[DL19Dataset] Loading queries using irdatasets...")
        dataset = ir_datasets.load("msmarco-passage/trec-dl-2019/judged")
        self.queries = []
        for q in dataset.queries_iter():
            self.queries.append((q[0], q[1]))

    def load_qrels(self):
        print("[DL19Dataset] Loading qrels using irdatasets...")
        dataset = ir_datasets.load("msmarco-passage/trec-dl-2019/judged")
        self.qrels = []
        for qrel in dataset.qrels_iter():
            self.qrels.append((qrel.query_id, qrel.doc_id, qrel.relevance))
        # qrels_file = args.qrels_file          # 来自 argument.py
        # print(f"[DL19Dataset] Loading qrels from {qrels_file}")
        # self.qrels = []
        # with open(qrels_file, 'r', encoding='utf-8') as f:
        #     for line in f:
        #         # TREC qrels 格式：query-id  iter  doc-id  relevance
        #         qid, _, docid, rel = line.strip().split()
        #         self.qrels.append((qid, docid, int(rel)))

if __name__=='__main__':
    # 测试DL19Dataset
    # 请根据实际文件路径修改下面的路径
    collection_path = Path(os.getcwd())/'MD25_DL19/corpus/collection.tsv'

    dataset = DL19Dataset(collection_path)
    dataset.load_collection()
    # print("Doc IDs:", dataset.doc_ids)
    # print("First 2 corpus entries:", dataset.corpus[:2])

    dataset.load_queries()
    print("Number of queries:", len(dataset.queries))
    print("First 2 queries:", dataset.queries[:2])

    dataset.load_qrels()
    print("Number of qrels:", len(dataset.qrels))
    print("First 2 qrels:", dataset.qrels[:2])