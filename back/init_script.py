import pickle
from datasets import load_dataset

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