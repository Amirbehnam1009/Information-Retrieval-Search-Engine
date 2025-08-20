# 🔍 Information Retrieval (IR) Search Engine – Persian Text

## 📖 Overview

This repository contains the implementation of a **Persian-language search engine**. The project builds a fully functional search engine capable of processing, indexing, and retrieving Persian news articles using both **vector space** and **Boolean retrieval models**.

The engine supports complex query types including **phrase search**, **negation**, and **TF-IDF-based ranking**, with additional optimizations like **champion lists** and **index elimination** for faster retrieval.

---

## 🧩 Project Phases

### ✅ Phase 1: Boolean Retrieval with Positional Index
- Data preprocessing: normalization, tokenization, stopword removal, stemming
- Building a **positional inverted index**
- Supporting queries with:
  - Simple terms
  - Phrases (`"phrase"`)
  - Negation (`NOT`)

### ✅ Phase 2: Vector Space Model & TF-IDF Ranking
- Document representation using **TF-IDF vectors**
- **Cosine similarity** for ranking
- Query processing in vector space
- Speed optimizations: **index elimination** and **champion lists**

### ⚡ Phase 3: Elasticsearch Integration (Bonus)
- Indexing and querying using **Elasticsearch**
- **Spelling correction** using n-gram suggesters
- **Synonym expansion** and **similarity modulation**
- **KNN-based document classification**

---

## 🚀 Features

### 📥 Data Loading & Preprocessing
- Loads Persian news dataset from JSON
- Applies:
  - ✅ Normalization
  - ✅ Tokenization
  - ✅ Stopword removal 🚫
  - ✅ Punctuation removal
  - ✅ Stemming (using `hazm` or custom stemmer)

### 📇 Indexing
- Builds **inverted index** with:
  - 📊 Term frequency (TF)
  - 📊 Document frequency (DF)
  - 📍 Positional information
- Supports **champion lists** for faster query processing

### 🔎 Searching
- Supports:
  - 🔤 Single-word queries
  - 💬 Phrase queries (`"..."`)
  - ❌ Negation queries (`!term`)
- Returns ranked results using **TF-IDF** or **term presence**

### 📊 Ranking & Retrieval
- 🏆 **Top-K retrieval** using TF-IDF scores
- 📐 **Cosine similarity** for vector model
- ⚡ Optional use of **champion lists** for speed

### 📈 Zipf’s Law Visualization
- 📉 Plots word frequency distributions to validate Zipf’s Law
- 🔁 Compares before/after stopword removal

### 💾 Index Persistence
- 💾 Save and load index to/from disk
- ⏩ Avoids re-indexing on reruns

---

## 🛠️ Installation & Usage

### Prerequisites
``` bash
pip install hazm numpy matplotlib
```
### Run the Project
```
bash
git clone https://github.com/Amirbehnam1009/Information-Retrieval-Search-Engine
cd Information-Retrieval-Search-Engine
python main.py
```
### Example Queries

``` bash
# Simple multi-word query
"اقتصاد ایران"

# Phrase query
"جام جهانی فوتبال"

# Negation query
تورم NOT کشور

# Complex combined query
"پزشکی سلامت" NOT دارو---
---

```
## 📁 Repository Structure
``` bash
Information-Retrieval-Search-Engine/
│
├── data/
│   └── news_data.json          # Persian news dataset
├── src/
│   ├── preprocess.py           # Text normalization & tokenization
│   ├── indexer.py              # Inverted index builder
│   ├── boolean_model.py        # Phase 1: Boolean retrieval
│   ├── vector_model.py         # Phase 2: TF-IDF & cosine similarity
│   ├── champion_list.py        # Champion list optimization
│   ├── elastic_integration.py  # Phase 3: Elasticsearch interface
│   └── utils.py                # Helper functions
├── reports/
│   ├── phase1_report.pdf       # Phase 1 detailed report
│   └── phase2_report.pdf       # Phase 2 detailed report
├── main.py                     # Main entry point
└── README.md
```
---

## 📊 Sample Outputs
* 📄 Ranked list of documents with titles, URLs, and snippets

* 🔍 Query-wise analysis of relevance

* 📉 Zipf’s Law and Heaps’ Law validation plots

* ⚡ Performance comparisons between Boolean and vector models
