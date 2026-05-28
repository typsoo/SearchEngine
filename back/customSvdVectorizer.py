from scipy.sparse.linalg import svds
import numpy as np


class CustomSvdVectorizer:
    def __init__(self, base_tfidf_vectorizer, k=100):
        self.base = base_tfidf_vectorizer
        self.k = k
        self.B = None
        self.norm_Ak = None
        self.U_k = None


    def fit(self):
        A_sparse = self.base.matrix.astype(float)


        U_k, S_k, Vt_k = svds(A_sparse, k=self.k)
        self.U_k = U_k

        D_k = np.diag(S_k)
        B = D_k @ Vt_k  
        self.B = B

        norm_Ak = np.linalg.norm(B, axis=0)
        norm_Ak[norm_Ak == 0] = 1e-9
        self.norm_Ak = norm_Ak

    def search(self, query_text, top_k=5):
        q_vector = self.base.transform_query(query_text)
        q_concept = q_vector @ self.U_k                        

        scores = q_concept @ self.B
        scores = scores / self.norm_Ak

        top_indices = np.argsort(scores)[-top_k:][::-1]
        return [(int(idx), float(scores[idx])) for idx in top_indices if scores[idx] > 0]