# SearchEngine

SearchEngine is a full-stack search engine project built to compare multiple information retrieval approaches on a Wikipedia-based document collection. The backend exposes a FastAPI endpoint that searches across prebuilt indexes, while the frontend provides a Next.js interface for querying and displaying ranked results.

Detailed implementation logic, architectural decisions, and step-by-step explanations are documented directly within the comments of the source code files.

## Dataset & Scale

To rigorously test the algorithms, the project scales beyond basic toy datasets:

- **Corpus:** 90,000 English Wikipedia articles, fetched and processed using the Hugging Face `datasets` library.
- **Vocabulary:** The extracted bag-of-words dictionary is strictly optimized and limited to 60,000 terms to maintain computational efficiency while preserving semantic depth.

## Technologies Used

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn
- python-dotenv
- NumPy
- SciPy
- scikit-learn
- NLTK
- rank-bm25
- Hugging Face `datasets`

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- ESLint

## Project Structure

### Backend files

- `back/main.py` - FastAPI application entry point. It defines the `/api/search` endpoint, configures CORS, selects the search algorithm, and returns search results with execution time.
- `back/search_engines.py` - Wrapper layer around the serialized search models. It loads the saved indexes from disk and formats raw ranking scores into API response objects.
- `back/init_script.py` - Dataset preparation and index-building script. It loads the Wikipedia corpus, trains all search models, and saves them as pickle files in `back/data`.
- `back/vectoraizers/baseVectorizer.py` - Shared base class for custom vectorizers. It handles tokenization, vocabulary building, document matrix storage, and generic search logic.
- `back/vectoraizers/customTfIdfVectorizer.py` - Custom TF-IDF implementation built from scratch.
- `back/vectoraizers/customBM25Vectorizer.py` - Custom BM25 implementation built from scratch.
- `back/vectoraizers/customSvdVectorizer.py` - Latent Semantic Indexing style model based on SVD over the custom TF-IDF matrix.
- `back/vectoraizers/library_vectorizers.py` - Library-based implementations using scikit-learn TF-IDF, Truncated SVD, and rank-bm25.

### Data folder

- `back/data/` stores the generated artifacts used by the backend at runtime.
- `doc_names.pkl` contains the Wikipedia document titles.
- `custom_tfidf.pkl`, `custom_bm25.pkl`, `custom_svd.pkl`, `lib_tfidf.pkl`, and `lib_bm25.pkl` store the trained search models.

## Mathematical Foundations

This project implements core Information Retrieval mathematics to compare different ranking strategies.

**1. Inverse Document Frequency (IDF)**
Used to reduce the weight of overly common words across the corpus:
$$IDF(w) = \log\frac{N}{n_w}$$
_(Where $N$ is the total number of documents and $n_w$ is the number of documents containing word $w$. Note: custom implementations use smoothed variations to prevent division by zero)._

**2. Cosine Similarity (Standard TF-IDF)**
Used as the primary metric to determine the relevance of a document vector ($d_j$) to a query vector ($q$):
$$\cos \theta_j = \frac{q^T d_j}{||q|| ||d_j||} = \frac{q^T A e_j}{||q|| ||A e_j||}$$
_Features like pre-normalized vectors (length = 1) are used to speed up runtime calculations._

**3. Latent Semantic Indexing (LSI / SVD)**
Singular Value Decomposition and low-rank approximation are applied to the term-document matrix $A$ to remove noise and capture hidden semantic relationships (synonyms):
$$A \simeq A_k = U_k D_k V_k^T = \sum_{i=1}^{k} \sigma_i u_i v_i^T$$
The similarity is then computed in this reduced semantic space to improve recall.

**4.BM25 Ranking**
An advanced probabilistic model that improves upon standard TF-IDF by introducing term frequency saturation (preventing the score from growing linearly with term frequency) and document length normalization:
$$score(D, Q) = \sum_{i=1}^{n} IDF(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{avgdl}\right)}$$
_Where $f(q_i, D)$ is the term frequency in the document, $|D|$ is the document length, and $avgdl$ is the average document length in the corpus. The parameters $k_1$ and $b$ control term saturation and length penalization, respectively._

## Search Algorithms

The project compares five retrieval approaches:

1. Custom TF-IDF
2. Custom BM25
3. Custom SVD / LSI
4. Library TF-IDF + Truncated SVD
5. Library BM25 using `rank-bm25`

The active algorithm is selected by the `algorithm` query parameter in the backend API. The search endpoint currently uses `top_k=8` when returning results.

## How to Run the Project

### 1. Backend setup

Create and activate a virtual environment, then install the Python dependencies:

```bash
cd back
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If the model files in `back/data/` are missing, build them first:

```bash
python init_script.py
```

Start the backend server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend setup

Install the frontend dependencies and start the development server:

```bash
cd ../front
bun install
bun run
```

### 3. Open the application

- Backend API: `http://localhost:8000`
- Frontend app: `http://localhost:3000`

## Notes

- The backend expects the generated pickle files in `back/data/`.
- The project is designed to compare classical search algorithms rather than neural retrieval models.
