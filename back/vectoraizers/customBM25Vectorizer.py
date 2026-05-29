import math
from collections import Counter
import numpy as np
from scipy.sparse import csc_matrix
from vectoraizers.baseVectorizer import BaseVectorizer

class CustomBM25Vectorizer(BaseVectorizer):
    """
    Implements the BM25 ranking function.
    BM25 improves upon standard TF-IDF by introducing term frequency saturation
    and document length normalization.
    """
    def __init__(self, max_features=None, k1=1.5, b=0.75):
        super().__init__(max_features)
        # TF saturation: higher = frequency matters more (0 = only presence matters)
        self.k1 = k1
        # length normalization: 0 = ignore length, 1 = fully penalize long docs
        self.b = b
        self.avgdl = 0.0 

    def fit_transform(self, documents):
        # 1. Parse documents and build vocabulary using the base class
        tokenized_docs, df_counts, top_words, total_length = self._build_base_vocab(documents)

        # Calculate the average document length (avgdl) across the entire corpus
        self.avgdl = total_length / self.num_docs if self.num_docs > 0 else 1.0

        # 2. Calculate BM25 specific Inverse Document Frequency (IDF)
        for word_idx, word in enumerate(top_words):
            self.vocab[word] = word_idx
            self.idx_to_word[word_idx] = word
            df = df_counts[word] 

            # Calculate Inverse Document Frequency (IDF) for each word
            # Formula: IDF(w) = log(N / n_w). Smoothing (+1) is added to prevent division by zero.
            idf_val = math.log(((self.num_docs - df + 0.5) / (df + 0.5)) + 1)

            # Clamp negative or zero IDFs for stop words that bypassed the filter
            self.idf[word_idx] = max(idf_val, 0.01)
            
        self.num_terms = len(self.vocab)
        
        rows, cols, data = [], [], []

        # 3. Build the Term-by-Document Sparse Matrix using BM25 TF formulation
        for doc_idx, tokens in enumerate(tokenized_docs):
            term_counts = Counter(tokens)
            doc_length = len(tokens)
            
            for word, count in term_counts.items():
                if word not in self.vocab: continue
                word_idx = self.vocab[word]
                
                # BM25 Term Frequency (Saturation and Length Normalization)
                numerator = count * (self.k1 + 1)
                denominator = count + self.k1 * (1 - self.b + self.b * (doc_length / self.avgdl))
                tf_bm25 = numerator / denominator
                
                rows.append(word_idx)
                cols.append(doc_idx)

                # Final score is IDF * BM25_TF
                data.append(self.idf[word_idx] * tf_bm25)

        # Store as a Compressed Sparse Column matrix
        self.matrix = csc_matrix((data, (rows, cols)), shape=(self.num_terms, self.num_docs))

    def transform_query(self, query_text):
        """
        Vectorizes the query.
        """
        tokens = self._clean_and_tokenize(query_text)
        term_counts = Counter(tokens)
        q_vector = np.zeros(self.num_terms)
        
        for word, count in term_counts.items():
            if word in self.vocab:
                word_idx = self.vocab[word]
                q_vector[word_idx] = count * self.idf[word_idx]
                
        return q_vector