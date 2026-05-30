import os
import time

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from search_engines import (
    CustomBm25Engine,
    CustomSvdEngine,
    CustomTfidfEngine,
    LibraryBm25Engine,
    LibraryTfidfEngine,
)

engines = {
    "custom_tfidf": CustomTfidfEngine(),
    "custom_bm25": CustomBm25Engine(),
    "custom_svd": CustomSvdEngine(),
    "lib_tfidf": LibraryTfidfEngine(),
    "lib_bm25": LibraryBm25Engine(),
}


load_dotenv()
app = FastAPI(title="Python Search Engine API")

frontend_url = os.getenv("FRONTEND_URL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url] if frontend_url else ["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["Accept"],
)


class SearchResultResponse(BaseModel):
    id: str
    title: str
    url: str
    snippet: str
    score: float


@app.get("/api/search", response_model=list[SearchResultResponse])
async def search(q: str, algorithm: str):
    start_time = time.time()
    engine = engines.get(algorithm.lower())
    raw_results = engine.search(query=q, top_k=8)

    execution_time = round(time.time() - start_time, 4)

    return JSONResponse(
        content={"results": raw_results, "executionTime": max(execution_time, 0.001)}
    )
