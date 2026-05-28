import re
import math
from collections import Counter
import nltk
from nltk.corpus import stopwords
import numpy as np
from scipy.sparse import csc_matrix
from abc import ABC, abstractmethod

nltk.download('stopwords', quiet=True)
ENGLISH_STOPWORDS = set(stopwords.words('english'))


class BaseVectorizer(ABC):
    def __init__(self, max_features=None):
        self.vocab = {}             
        self.idx_to_word = {}       
        self.idf = {}               
        self.matrix = None          
        self.num_docs = 0
        self.num_terms = 0
        self.max_features = max_features    

    @staticmethod
    def _clean_and_tokenize(text):
        words = re.findall(r'\b[a-z]+\b', text.lower())
        return [w for w in words if w not in ENGLISH_STOPWORDS]

    def _build_base_vocab(self, documents):
        self.num_docs = len(documents)
        tokenized_docs = []
        df_counts = Counter() 
        tf_counts = Counter() 
        total_length = 0
        
        for doc in documents:
            tokens = self._clean_and_tokenize(doc)
            tokenized_docs.append(tokens)
            df_counts.update(set(tokens)) 
            tf_counts.update(tokens)
            total_length += len(tokens)
            
        if self.max_features is None:
            top_words = list(tf_counts.keys())
        else:
            top_words = [word for word, _ in tf_counts.most_common(self.max_features)]
            
        return tokenized_docs, df_counts, top_words, total_length

    def search(self, query_text, top_k=5):
        q_vector = self.transform_query(query_text)
        scores = q_vector @ self.matrix
        top_indices = np.argsort(scores)[-top_k:][::-1]
        return [(int(idx), float(scores[idx])) for idx in top_indices if scores[idx] > 0]

    @abstractmethod
    def fit_transform(self, documents):
        pass

    @abstractmethod
    def transform_query(self, query_text):
        pass