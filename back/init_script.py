"""
Initialization and Index Building Script for the Search Engine.

This script performs the heavy lifting required before the backend server can start.
It acts with the following steps:
1. Downloads a large-scale dataset (90,000 English Wikipedia articles) using Hugging Face datasets.
2. Extracts document texts and titles.
3. Initializes, trains , and builds the vocabulary for 5 different 
   Information Retrieval algorithms:
   - Custom TF-IDF
   - Custom Okapi BM25
   - Custom Latent Semantic Indexing (SVD)
   - Library-based TF-IDF + SVD (scikit-learn)
   - Library-based BM25 (rank_bm25)
4. Serializes (pickles) the trained models and document titles to disk (./data/ directory).

By running this script once, the FastAPI application can quickly load the pre-computed 
matrices and models into RAM without having to rebuild the index on every startup.
"""

import pickle
from datasets import load_dataset
import nltk

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

from vectoraizers.customTfIdfVectorizer import CustomTfidfVectorizer
from vectoraizers.customBM25Vectorizer import CustomBM25Vectorizer
from vectoraizers.customSvdVectorizer import CustomSvdVectorizer
from vectoraizers.library_vectorizers import LibraryTfidfVectorizer, LibraryBm25Vectorizer


print("Loading dataset...")
dataset = load_dataset("wikimedia/wikipedia", "20231101.en", split="train[:90000]", trust_remote_code=False)
documents = dataset["text"]
doc_names = dataset["title"]

with open("./data/doc_names.pkl", "wb") as f:
    pickle.dump(doc_names, f)

print("\nTraining Custom TF-IDF...")
custom_tfidf = CustomTfidfVectorizer(max_features=60000)
custom_tfidf.fit_transform(documents)
with open("./data/custom_tfidf.pkl", "wb") as f:
    pickle.dump(custom_tfidf, f)

print("\nTraining Custom BM25...")
custom_bm25 = CustomBM25Vectorizer(max_features=60000)
custom_bm25.fit_transform(documents)
with open("./data/custom_bm25.pkl", "wb") as f:
    pickle.dump(custom_bm25, f)

print("\nTraining Custom SVD (LSI)...")
custom_svd = CustomSvdVectorizer(base_tfidf_vectorizer=custom_tfidf, k=150)
custom_svd.fit()
with open("./data/custom_svd.pkl", "wb") as f:
    pickle.dump(custom_svd, f)

print("\nTraining Library Sklearn TF-IDF...")
lib_tfidf = LibraryTfidfVectorizer()
lib_tfidf.fit_transform(documents)
with open("./data/lib_tfidf.pkl", "wb") as f:
    pickle.dump(lib_tfidf, f)

print("\nTraining Library Rank_BM25...")
lib_bm25 = LibraryBm25Vectorizer()
lib_bm25.fit_transform(documents)
with open("./data/lib_bm25.pkl", "wb") as f:
    pickle.dump(lib_bm25, f)

print("\nAll 5 indexes successfully built and saved!")