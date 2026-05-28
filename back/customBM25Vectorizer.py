import math
from collections import Counter
import numpy as np
from scipy.sparse import csc_matrix
from baseVectorizer import BaseVectorizer

class CustomBM25Vectorizer(BaseVectorizer):
    def __init__(self, max_features=None, k1=1.5, b=0.75):
        super().__init__(max_features)
        self.k1 = k1
        self.b = b
        self.avgdl = 0.0 

    def fit_transform(self, documents):
        tokenized_docs, df_counts, top_words, total_length = self._build_base_vocab(documents)
        self.avgdl = total_length / self.num_docs if self.num_docs > 0 else 1.0
        for word_idx, word in enumerate(top_words):
            self.vocab[word] = word_idx
            self.idx_to_word[word_idx] = word
            df = df_counts[word] 
            idf_val = math.log(((self.num_docs - df + 0.5) / (df + 0.5)) + 1)
            self.idf[word_idx] = max(idf_val, 0.01)
            
        self.num_terms = len(self.vocab)
        
        rows, cols, data = [], [], []

        for doc_idx, tokens in enumerate(tokenized_docs):
            term_counts = Counter(tokens)
            doc_length = len(tokens)
            
            for word, count in term_counts.items():
                if word not in self.vocab: continue
                word_idx = self.vocab[word]
                
                numerator = count * (self.k1 + 1)
                denominator = count + self.k1 * (1 - self.b + self.b * (doc_length / self.avgdl))
                tf_bm25 = numerator / denominator
                
                rows.append(word_idx)
                cols.append(doc_idx)
                data.append(self.idf[word_idx] * tf_bm25)

        self.matrix = csc_matrix((data, (rows, cols)), shape=(self.num_terms, self.num_docs))

    def transform_query(self, query_text):
        tokens = self._clean_and_tokenize(query_text)
        term_counts = Counter(tokens)
        q_vector = np.zeros(self.num_terms)
        
        for word, count in term_counts.items():
            if word in self.vocab:
                word_idx = self.vocab[word]
                q_vector[word_idx] = count * self.idf[word_idx]
                
        return q_vector