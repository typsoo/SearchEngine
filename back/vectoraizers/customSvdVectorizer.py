from scipy.sparse.linalg import svds
import numpy as np


class CustomSvdVectorizer:
    """
    Wraps an existing TF-IDF vectorizer to transform its sparse term-document 
    matrix into a dense, lower-dimensional "concept" space.
    """
    def __init__(self, base_tfidf_vectorizer, k=100):
        self.base = base_tfidf_vectorizer
        self.k = k
        self.B = None         # Document representations in latent space
        self.norm_Ak = None   # Precomputed norms of document vectors for fast cosine similarity
        self.U_k = None       # Term-to-concept projection matrix


    def fit(self):
        """
        Step 8: Perform truncated SVD on the base TF-IDF matrix.
        Decomposes A into U * S * V^T, keeping only the top 'k' singular values.
        """

        # SVD requires float operations, convert sparse matrix if needed
        A_sparse = self.base.matrix.astype(float)

        # svds is highly optimized for sparse matrices.
        # Returns U_k (terms to concepts), S_k (singular values), Vt_k (concepts to docs)
        U_k, S_k, Vt_k = svds(A_sparse, k=self.k)
        self.U_k = U_k

        # Convert the 1D array of singular values into a diagonal matrix D_k
        D_k = np.diag(S_k)

        # Calculate the document representation in the latent space (B matrix)
        # Instead of explicitly forming the massive dense matrix A_k, we store B = D_k * V_k^T

        # OPTIMIZATION NOTE:
        # I explicitly avoid calculating the full dense matrix A_k = U_k @ D_k @ Vt_k.
        # For a large dataset it will be hard to compute.
        # Instead, I compute and store only B = D_k @ Vt_k. The associative property of 
        # matrix multiplication allows us to achieve the exact same result during search
        # by projecting the query into the latent space first.
        B = D_k @ Vt_k  
        self.B = B

        # Precompute the lengths (norms) of each document vector in the latent space.
        norm_Ak = np.linalg.norm(B, axis=0)
        norm_Ak[norm_Ak == 0] = 1e-9
        self.norm_Ak = norm_Ak

    def search(self, query_text, top_k=5):
        """
        Executes a search query in the reduced latent space.
        Formula applied: cosine = (q^T * U_k * D_k * V_k^T) / (||q|| * ||d_j||)
        """

        # 1. Transform text into a standard TF-IDF vector using the base vectorizer
        q_vector = self.base.transform_query(query_text)

        # 2. Project the raw query vector into the latent concept space (q^T * U_k)
        q_concept = q_vector @ self.U_k                        

        # 3. Calculate the final dot product using the precomputed B matrix.
        # This effectively calculates (q^T * U_k) * (D_k * V_k^T) without building A_k.
        scores = q_concept @ self.B

        # 4. Normalize by document lengths to get final Cosine Similarity
        scores = scores / self.norm_Ak

        # 5. Sort and return the top_k results
        top_indices = np.argsort(scores)[-top_k:][::-1]
        return [(int(idx), float(scores[idx])) for idx in top_indices if scores[idx] > 0]