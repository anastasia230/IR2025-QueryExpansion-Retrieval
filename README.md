# IR2025 - Query Expansion and Information Retrieval

This is the final project for the *Information Retrieval* course (AUEB, 2025).  
It implements a three-phase pipeline for document indexing, retrieval, and query expansion using **ElasticSearch** and **WordNet**, with evaluation based on the **TREC-COVID** dataset.

## 🔍 Project Overview

### ✅ Phase 1: Baseline Retrieval with ElasticSearch

- Index documents using ElasticSearch.
- Perform classic keyword-based retrieval without query expansion.
- Evaluate using `trec_eval`.

**Key Files:**
- `index_documents.py`: Indexes the corpus in ElasticSearch.
- `search_documents.py`: Executes keyword search over the index.
- `results_k20.run`, `results_k30.run`, `results_k50.run`: Output files for evaluation.

---

### 🔁 Phase 2: Query Expansion with WordNet (NLTK)

- Expand user queries with **synonyms and hypernyms** using **WordNet** via NLTK.
- Perform retrieval with expanded queries.
- Compare with baseline performance using `trec_eval`.

**Key Files:**
- `expand_queries.py`: Expands each query using WordNet.
- `search_expanded_queries.py`: Runs search with expanded queries.
- `results_expanded_k20.run`, `results_expanded_hyper_k20.run`: Expanded run files for evaluation.

---

### 🤖 Phase 3: Word Embeddings (Word2Vec)

- Train or load Word2Vec embeddings.
- Expand queries with most similar terms from the embedding space.
- Evaluate retrieval results.

**Key Files:**
- `expand_queries_word2vec.py`: Query expansion using Word2Vec similarities.
- `search_word2vec.py`: Runs search using word2vec-expanded queries.
- `results_word2vec_k20.run`: Retrieval results for evaluation.

> ⚠️ **Note**: Some large files like `corpus.jsonl` (211MB) and parts of the ElasticSearch installation were **not uploaded** due to GitHub's file size limits. See below.

---

## 📦 Not Included Due to Size

The following files were excluded from the Git repo due to GitHub's 100MB file size limit:

| File | Size | Notes |
|------|------|-------|
| `phase3/corpus.jsonl` or `trec-covid/corpus.jsonl` | ~211MB | Main document corpus (TREC-COVID dataset) |
| `elasticsearch-8.17.2/jdk/lib/modules` | ~134MB | Java runtime modules |
| `elasticsearch-8.17.2/modules/x-pack-ml/platform/windows-x86_64/bin/torch_cpu.dll` | ~116MB | Native Torch binary |

👉 These files are referenced in the `.gitignore`. Please download them separately if needed for reproduction.

---

## 📂 Folder Structure
IR2025-QueryExpansion-Retrieval/
│
├── phase1/ # Classic IR with keyword search
│ ├── index_documents.py
│ ├── search_documents.py
│ ├── results_k20.run
│ └── ...
│
├── phase2/ # Query expansion with WordNet
│ ├── expand_queries.py
│ ├── search_expanded_queries.py
│ ├── results_expanded_k20.run
│ ├── results_expanded_hyper_k20.run
│ └── ...
│
├── phase3/ # Word2Vec-based expansion
│ ├── expand_queries_word2vec.py
│ ├── search_word2vec.py
│ └── results_word2vec_k20.run
│
├── trec_eval/ # Evaluation tool
│ └── trec_eval-9.0.7/
│
├── trec-covid/ # Evaluation and corpus files
│ ├── qrels-covid_d5_judgments.txt
│ ├── topics-covid19.xml
│ └── corpus.jsonl ⚠️ (excluded)
│
├── wordnetfiles/ # WordNet dictionary files (optional)
│ └── ... (can be ignored if using NLTK WordNet API)
│
├── .gitignore


## 🧪 Evaluation

All runs were evaluated using:

- [`trec_eval`](https://github.com/usnistgov/trec_eval): Official tool for evaluating retrieval systems
- Metrics: `map`, `P@10`, `ndcg`, `recall`, etc.
- Queries: Derived from `topics-covid19.xml`
- Relevance judgments: `qrels-covid_d5_judgments.txt`

---

## 🛠 Setup Instructions

1. Install dependencies (Python, NLTK, gensim, ElasticSearch)
2. Download TREC-COVID corpus and unpack it into `trec-covid/`
3. Run indexing: `python index_documents.py`
4. Run baseline or expansion scripts depending on phase
5. Evaluate with `trec_eval`:
   ```bash
   ./trec_eval -q qrels-covid_d5_judgments.txt results_k20.run

Notes

Query expansion can greatly improve recall, but may lower precision if not filtered.

Word2Vec embeddings were either trained on the corpus or loaded from pretrained vectors.

ElasticSearch version used: 8.17.2

Author
Anastasia Andromida
Course: Information Retrieval (IR2025)
Institution: Athens University of Economics and Business (AUEB)
