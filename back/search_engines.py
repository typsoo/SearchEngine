import pickle
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseEngine(ABC):
    def __init__(self):
        with open("./data/doc_names.pkl", "rb") as f:
            self.doc_names = pickle.load(f)
            
    @abstractmethod
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        pass

    def _format_results(self, raw_results, algorithm_name: str) -> List[Dict[str, Any]]:
        response = []
        for doc_idx, score in raw_results:
            response.append({
                "id": f"doc_{doc_idx}",
                "title": self.doc_names[doc_idx],
                "url": f"https://en.wikipedia.org/wiki/{self.doc_names[doc_idx]}",
                "snippet": f"Find by {algorithm_name}.",
                "score": float(score)
            })
        return response


class CustomTfidfEngine(BaseEngine):
    def __init__(self):
        super().__init__()
        with open("./data/custom_tfidf.pkl", "rb") as f:
            self.model = pickle.load(f)

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        raw_results = self.model.search(query, top_k=top_k)
        return self._format_results(raw_results, "Custom_TF-IDF")

class CustomBm25Engine(BaseEngine):
    def __init__(self):
        super().__init__()
        with open("./data/custom_bm25.pkl", "rb") as f:
            self.model = pickle.load(f)

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        raw_results = self.model.search(query, top_k=top_k)
        return self._format_results(raw_results, "CustomBM25")
    

class CustomSvdEngine(BaseEngine):
    def __init__(self):
        super().__init__()
        with open("./data/custom_svd.pkl", "rb") as f:
            self.model = pickle.load(f)
    def search(self, query: str, top_k: int = 5):
        return self._format_results(self.model.search(query, top_k), "Custom SVD (LSI)")


class LibraryTfidfEngine(BaseEngine):
    def __init__(self):
        super().__init__()
        with open("./data/lib_tfidf.pkl", "rb") as f:
            self.model = pickle.load(f)
    def search(self, query: str, top_k: int = 5):
        return self._format_results(self.model.search(query, top_k), "Sklearn TF-IDF")

class LibraryBm25Engine(BaseEngine):
    def __init__(self):
        super().__init__()
        with open("./data/lib_bm25.pkl", "rb") as f:
            self.model = pickle.load(f)
    def search(self, query: str, top_k: int = 5):
        return self._format_results(self.model.search(query, top_k), "Rank_BM25")