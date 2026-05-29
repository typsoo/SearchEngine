import re
from collections import Counter
from nltk.corpus import stopwords
import numpy as np
from abc import ABC, abstractmethod


# Cache the set of English stop words for fast O(1) lookups during tokenization
ENGLISH_STOPWORDS = set(stopwords.words('english'))


class BaseVectorizer(ABC):
    """
    Abstract base class for all search vectorizers.
    Provides shared utilities for text cleaning, tokenization, vocabulary building,
    and executing cosine similarity searches.
    """
    def __init__(self, max_features=None):
        self.vocab = {}             # Maps word (string) -> column index (int)
        self.idx_to_word = {}       # Maps column index (int) -> word (string)
        self.idf = {}               # Maps column index (int) -> IDF weight (float)
        self.matrix = None          # The final term-by-document sparse matrix
        self.num_docs = 0           # Total number of documents (N)
        self.num_terms = 0          # Total number of unique terms in vocabulary
        self.max_features = max_features  # Optional cap on vocabulary size

    @staticmethod
    def _clean_and_tokenize(text):
        """
        Cleans the input text and splits it into tokens.
        - Extracts only alphabetical words using regex.
        - Converts everything to lowercase.
        - Removes common meaningless English stop words.
        """
        words = re.findall(r'\b[a-z]+\b', text.lower())
        return [w for w in words if w not in ENGLISH_STOPWORDS]

    def _build_base_vocab(self, documents):
        """
        Step 2 of the lab: Vocabulary extraction.
        Scans all documents to build the global dictionary and count term frequencies.
        
        Returns:
            tokenized_docs: List of tokenized documents.
            df_counts: Document Frequency (in how many docs does a word appear).
            top_words: The final list of words to be included in the vocabulary.
            total_length: Total number of tokens across all documents.
        """
        self.num_docs = len(documents)
        tokenized_docs = []
        df_counts = Counter()  # DF: Number of documents containing the word
        tf_counts = Counter()  # TF: Total occurrences of the word globally
        total_length = 0
        
        for doc in documents:
            tokens = self._clean_and_tokenize(doc)
            tokenized_docs.append(tokens)

            # Use set(tokens) so a word is counted only once per document for DF
            df_counts.update(set(tokens)) 
            tf_counts.update(tokens)
            total_length += len(tokens)
            
        # Limit vocabulary size if max_features is specified (controls matrix size)
        if self.max_features is None:
            top_words = list(tf_counts.keys())
        else:
            top_words = [word for word, _ in tf_counts.most_common(self.max_features)]
            
        return tokenized_docs, df_counts, top_words, total_length

    def search(self, query_text, top_k=5):
        """
        Step 6 & 7 of the lab: Search and Cosine Similarity calculation.
        Since both the query vector and document matrix are pre-normalized to length 1,
        the cosine similarity formula simplifies to a direct dot product (q^T * A).
        """
        # Convert raw text into a normalized feature vector
        q_vector = self.transform_query(query_text)
        
        # Fast matrix multiplication: computes cosine similarity for all docs instantly
        scores = q_vector @ self.matrix
        
        # Get indices of the top_k highest scores, sorted in descending order
        top_indices = np.argsort(scores)[-top_k:][::-1]
        
        # Return tuples of (document_id, similarity_score), excluding zero matches
        return [(int(idx), float(scores[idx])) for idx in top_indices if scores[idx] > 0]

    @abstractmethod
    def fit_transform(self, documents):
        """Must be implemented by subclasses to build the specific document matrix."""
        pass

    @abstractmethod
    def transform_query(self, query_text):
        """Must be implemented by subclasses to vectorize the search query."""
        pass