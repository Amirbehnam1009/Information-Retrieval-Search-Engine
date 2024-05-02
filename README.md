# Information-Retrieval-Search-Engine

## Overview

This project is a culmination of an Information Retrieval Course, dedicated to the development of an advanced Persian search engine. Utilizing a vast dataset comprising documents sourced from a Persian news agency, the primary goal is to enhance search capabilities for Persian language users.


## Features

### Data Loading and Preprocessing
- Load dataset from a JSON file and preprocess it seamlessly.
- Includes normalization, tokenization, stopwords removal, punctuation elimination, and stemming for optimal data quality.

### Indexing
- Establishes an inverted index of the dataset, capturing word occurrences.
- Stores word frequency, document frequency, and positional data within documents.
- Integrates a champion list mechanism for streamlined search operations.

### Searching
- Versatile search capabilities:
  - Single-word queries
  - Phrasal queries (enclosed in double quotes)
  - Negation queries (using '!' for exclusion)
- Ranks results based on relevance using TF-IDF scoring.

### Ranking and Retrieval
- Facilitates ranked retrieval functionality for top-k most relevant documents.
- Utilizes TF-IDF scores for ranking.
- Optionally employs champion lists for expedited retrieval.

### Zipf's Law Visualization
- Generates Zipf's Law plots to visualize word frequency distribution within the dataset.
- Provides insights into underlying data patterns and characteristics.

### Index Saving and Loading
- Seamless saving and loading of the index to/from a file.
- Enhances efficiency, especially with large datasets, by eliminating repeated indexing processes.





