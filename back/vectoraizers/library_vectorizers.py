from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
import numpy as np
import nltk

nltk.download('punkt', quiet=True)

class LibraryTfidfVectorizer:
    def __init__(self, k=200):
        self.stemmer = SnowballStemmer("english")
        self.k = k
        
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            lowercase=True,
            min_df=2,
            max_df=0.8,
            max_features=25000,
            tokenizer=self._stem_tokenizer,
            token_pattern=None,
            ngram_range=(1, 2),

        )
        
        self.svd_model = TruncatedSVD(n_components=self.k, random_state=42)
        self.documents_matrix = None

    def _stem_tokenizer(self, text):
        tokens = word_tokenize(text.lower())
        return [self.stemmer.stem(word) for word in tokens if word.isalpha()]

    def fit_transform(self, documents):
        tfidf_sparse_matrix = self.vectorizer.fit_transform(documents)

        self.documents_matrix = self.svd_model.fit_transform(tfidf_sparse_matrix)


    def search(self, query_text, top_k=5):
        query_vector = self.vectorizer.transform([query_text])

        query_vector = self.svd_model.transform(query_vector)

        similarities = cosine_similarity(query_vector, self.documents_matrix)[0]

        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return [(int(idx), float(similarities[idx])) for idx in top_indices if similarities[idx] > 0]


class LibraryBm25Vectorizer:
    def __init__(self):
        self.stemmer = SnowballStemmer("english")
        self.analyzer  = None

        self.text_processor = CountVectorizer(
            stop_words='english',
            lowercase=True,
            tokenizer=self._stem_tokenizer,
            token_pattern=None,
            ngram_range=(1, 2),   

        )
        self.bm25 = None

    def _stem_tokenizer(self, text):
        tokens = word_tokenize(text.lower())
        return [self.stemmer.stem(word) for word in tokens if word.isalpha()]

    def fit_transform(self, documents):
        self.analyzer = self.text_processor.build_analyzer()
        tokenized_corpus = [self.analyzer(doc) for doc in documents]

        self.bm25 = BM25Okapi(tokenized_corpus)

    def search(self, query_text, top_k=5):
        query_tokens = self.analyzer(query_text)
        scores = self.bm25.get_scores(query_tokens)

        top_indices = np.argsort(scores)[-top_k:][::-1]
        return [(int(idx), float(scores[idx])) for idx in top_indices if scores[idx] > 0]