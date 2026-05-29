import math
from collections import Counter
import numpy as np
from scipy.sparse import csc_matrix
from vectoraizers.baseVectorizer import BaseVectorizer

class CustomTfidfVectorizer(BaseVectorizer):
    """
    Implements a classic TF-IDF search engine.
    Builds a sparse term-by-document matrix and pre-normalizes vectors
    to optimize cosine similarity calculations.
    """
    def fit_transform(self, documents):
        # 1. Parse documents and extract global vocabulary
        tokenized_docs, df_counts, top_words, _ = self._build_base_vocab(documents)


        # 2. Calculate Inverse Document Frequency (IDF) for each word
        # Formula: IDF(w) = log(N / n_w). Smoothing (+1) is added to prevent division by zero.
        for word_idx, word in enumerate(top_words):
            self.vocab[word] = word_idx
            self.idx_to_word[word_idx] = word
            df = df_counts[word]
            self.idf[word_idx] = math.log((self.num_docs + 1) / (df + 1)) + 1
            
        self.num_terms = len(self.vocab)

        # 3. Build the Term-by-Document Sparse Matrix
        # I use coordinate lists (rows, cols, data) to construct a SciPy CSC matrix efficiently
        rows, cols, data = [], [], []
        doc_norms = np.zeros(self.num_docs)

        for doc_idx, tokens in enumerate(tokenized_docs):
            term_counts = Counter(tokens)
            doc_sq_sum = 0.0
            for word, count in term_counts.items():
                if word not in self.vocab: continue

                word_idx = self.vocab[word]
                # Calculate TF-IDF weight for this specific word in this document
                tfidf_score = count * self.idf[word_idx]
                
                rows.append(word_idx)
                cols.append(doc_idx)
                data.append(tfidf_score)

                # Accumulate squared sum to calculate vector length (Euclidean norm) later
                doc_sq_sum += tfidf_score ** 2
            
            # Prevent division by zero for empty documents
            doc_norms[doc_idx] = max(math.sqrt(doc_sq_sum), 1e-9)

        # 4. Pre-normalize all document vectors to length 1 (Step 7 of the lab)
        # This allows replacing expensive cosine similarity logic with a simple dot product
        data = np.array(data) / doc_norms[cols]

        # Create Compressed Sparse Column (CSC) matrix for fast column-based math operations
        self.matrix = csc_matrix((data, (rows, cols)), shape=(self.num_terms, self.num_docs))

    def transform_query(self, query_text):
        """
        Step 6: Converts the user's search text into a TF-IDF vector[cite: 23].
        Applies the exact same vocabulary, IDF weights, and length normalization as the documents.
        """
        tokens = self._clean_and_tokenize(query_text)
        term_counts = Counter(tokens)
        q_vector = np.zeros(self.num_terms)

        # Build the query vector using existing IDF weights
        for word, count in term_counts.items():
            if word in self.vocab:
                word_idx = self.vocab[word]
                q_vector[word_idx] = count * self.idf[word_idx]

        # Normalize the query vector to length 1 [cite: 27]
        q_norm = np.linalg.norm(q_vector)
        if q_norm > 0: q_vector = q_vector / q_norm
        return q_vector