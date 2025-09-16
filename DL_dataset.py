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
        collection是什么？
        collection是一个包含所有文档的文件，通常为collection.tsv。每一行包含一个文档ID和对应的文档内容，格式如下：
        docid \t text
        例如：
        123456 \t This is the content of the document.
        234567 \t Another document content here.

        本方法会读取collection文件，将所有文档的ID存入self.doc_ids，将文档内容（分词后的小写单词列表）存入self.corpus。
        """
        print("[DL19Dataset] Loading collection...")
        with open(self.collection_path, 'r', encoding='utf8') as f:
            reader = csv.reader(f, delimiter='\t')
            for i, row in enumerate(reader):
                docid, text = row[0], row[1]
                self.doc_ids.append(docid)
                self.corpus.append(text.lower().split())
        print(f"Loaded {len(self.corpus)} documents.")

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