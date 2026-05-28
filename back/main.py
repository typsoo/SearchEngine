import time
import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

from search_engines import CustomBm25Engine, CustomTfidfEngine, CustomSvdEngine, LibraryBm25Engine, LibraryTfidfEngine

engines = {
    "custom_tfidf": CustomTfidfEngine(),
    "custom_bm25": CustomBm25Engine(),
    "custom_svd": CustomSvdEngine(),
    "lib_tfidf": LibraryTfidfEngine(),
    "lib_bm25": LibraryBm25Engine()
}



load_dotenv()
app = FastAPI(title="Python Search Engine API")

frontend_url = os.getenv("FRONTEND_URL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchResultResponse(BaseModel):
    id: str
    title: str
    url: str
    snippet: str
    score: float

@app.get("/api/search", response_model=List[SearchResultResponse])
async def search(
    q: str = Query(..., description="Поисковый запрос"),
    algorithm: str = Query("tfidf", description="Алгоритм поиска")
):
    start_time = time.time()
    engine = engines.get(algorithm.lower())
    raw_results = engine.search(query=q, top_k=5)

    
    execution_time = round(time.time() - start_time, 4)
    
        
    return JSONResponse(content={
        "results": raw_results,
        "executionTime": max(execution_time, 0.001)
    })