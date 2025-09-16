**# 实验相关说明

## 遇到的问题

- "Unable to find javac" 错误，是 Pyserini 在调用 Java 相关功能（如 pyserini.eval.trec_eval）时，找不到 Java 编译器（javac） 导致的。
  这是因为 Pyserini 底层依赖 jnius 实现 Python 与 Java 的交互，而 jnius 需要完整的 JDK（不仅仅是 JRE） 才能正常工作。
- 由于加载DL19需要加载docs，整个文档的体积在34.6G，下载需要180h，所以这里采用与训练的DL19_md25。
- (lvhang) (base) rqyang@a100:~/MD25_DL9/trec_dl19_data$ wget https://msmarco.blob.core.windows.net/msmarcoranking/collection.tar.gz
  --2025-09-14 10:12:59--  https://msmarco.blob.core.windows.net/msmarcoranking/collection.tar.gz
  正在解析主机 msmarco.blob.core.windows.net (msmarco.blob.core.windows.net)... 20.150.34.4
  正在连接 msmarco.blob.core.windows.net (msmarco.blob.core.windows.net)|20.150.34.4|:443... 已连接。
  已发出 HTTP 请求，正在等待回应... 409 Public access is not permitted on this storage account.
  2025-09-14 10:13:01 错误 409：Public access is not permitted on this storage account.。
- https://microsoft.github.io/msmarco/TREC-Deep-Learning-2019

## corpus结构

/home/rqyang/MD25_DL19/corpus

```
├── msmarco-passagetest2019-top1000.tsv.gz
├── msmarco-passagetest2019-top1000.tsv
├── collection.tar.gz
├── collection.tsv
├── MS MARCO Docs.tsv
└── MS MARCO Docs.tsv.gz
```

## 实验记录

**collection.tsv**
| 设置 | bm25\_k1 | bm25\_b | top\_k | RR\@10 | AP\@1000 | nDCG\@10 |
| ------ | ---------- | --------- | -------- | -------- | ---------- | ---------- |
| 1    | 1.5      | 0.75    | 1000   | 0.7039 | 0.2226   | 0.3779   |
| 2    | 0.82     | 0.68    | 100    | 0.7212 | 0.2058   | 0.4139   |
| 3    | 0.82     | 0.68    | 1000   | 0.7212 | 0.2493   | 0.4139   |
| 4    | 0.9      | 0.4     | 100    | 0.7508 | 0.2043   | 0.4266   |
| 5    | 0.9      | 0.68    | 100    | 0.7204 | 0.2034   | 0.4119   |
| 6    | 0.9      | 0.3     | 100    | 0.7388 | 0.2023   | 0.4242   |
| 7    | 0.95     | 0.4     | 100    | 0.7508 | 0.2026   | 0.4196   |
| 8    | 0.95     | 0.3     | 100    | 0.7643 | 0.2010   | 0.4229   |
| 9    | 0.95     | 0.26    | 100    | 0.7620 | 0.1998   | 0.4232   |
| 10   | 0.95     | 0.23    | 100    | 0.7507 | 0.1983   | 0.4191   |
| 11   | 0.5      | 0.23    | 100    | 0.7277 | 0.2137   | 0.4257   |
| 12   | 0.4      | 0.23    | 100    | 0.7141 | 0.2166   | 0.4248   |
| 13   | 0.6      | 0.23    | 100    | 0.7419 | 0.2114   | 0.4309   |
| 14   | 0.7      | 0.23    | 100    | 0.7416 | 0.2070   | 0.4299   |


**msmarco-passagetest2019-top1000.tsv**
| 设置 | bm25\_k1 | bm25\_b | top\_k | RR\@10 | AP\@1000 | nDCG\@10 |
| ------ | ---------- | --------- | -------- | -------- | ---------- | ---------- |
| 1   | 0.9 | 0.68 | 100 | 0.7567 | 0.2268 | 0.4206 |
| 2   | 0.6 | 0.68 | 100 | 0.7296 | 0.2337 | 0.4227 |
| 3   | 0.5 | 0.68 | 100 | 0.7257 | 0.2365 | 0.4270 |
| 4   | 0.4 | 0.68 | 100 | 0.7275 | 0.2397 | 0.4306 |
| 5   | 0.3 | 0.68 | 100 | 0.7267 | 0.2411 | 0.4370 |
| 6   | 0.2 | 0.68 | 100 | 0.7246 | 0.2400 | 0.4309 |
| 7   | 0.3 | 0.4  | 100 | 0.6917 | 0.2401 | 0.4305 |
| 8   | 0.3 | 0.5  | 100 | 0.7045 | 0.2407 | 0.4352 |
| 9   | 0.3 | 0.75 | 100 | 0.7270 | 0.2404 | 0.4360 |
| 10  | 0.3 | 0.75 | 100 | 0.7270 | 0.2404 | 0.4360 |
