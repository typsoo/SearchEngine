import math
from collections import Counter
import numpy as np
from scipy.sparse import csc_matrix
from baseVectorizer import BaseVectorizer

class CustomTfidfVectorizer(BaseVectorizer):
    def fit_transform(self, documents):
        tokenized_docs, df_counts, top_words, _ = self._build_base_vocab(documents)

        for word_idx, word in enumerate(top_words):
            self.vocab[word] = word_idx
            self.idx_to_word[word_idx] = word
            df = df_counts[word]
            self.idf[word_idx] = math.log((self.num_docs + 1) / (df + 1)) + 1
            
        self.num_terms = len(self.vocab)

        
        rows, cols, data = [], [], []
        doc_norms = np.zeros(self.num_docs)

        for doc_idx, tokens in enumerate(tokenized_docs):
            term_counts = Counter(tokens)
            doc_sq_sum = 0.0
            for word, count in term_counts.items():
                if word not in self.vocab: continue
                word_idx = self.vocab[word]
                tfidf_score = count * self.idf[word_idx]
                
                rows.append(word_idx)
                cols.append(doc_idx)
                data.append(tfidf_score)
                doc_sq_sum += tfidf_score ** 2
                
            doc_norms[doc_idx] = max(math.sqrt(doc_sq_sum), 1e-9)

        data = np.array(data) / doc_norms[cols]
        self.matrix = csc_matrix((data, (rows, cols)), shape=(self.num_terms, self.num_docs))

    def transform_query(self, query_text):
        tokens = self._clean_and_tokenize(query_text)
        term_counts = Counter(tokens)
        q_vector = np.zeros(self.num_terms)

        for word, count in term_counts.items():
            if word in self.vocab:
                word_idx = self.vocab[word]
                q_vector[word_idx] = count * self.idf[word_idx]

        q_norm = np.linalg.norm(q_vector)
        if q_norm > 0: q_vector = q_vector / q_norm
        return q_vector