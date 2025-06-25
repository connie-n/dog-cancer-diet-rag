from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from retriever import retrieve_similar_docs
from llm_agent import generate_answer_with_cache
import uvicorn
from db_logger import log_query
import logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    try:
        docs = retrieve_similar_docs(request.query, top_k=3)
        answer = generate_answer_with_cache(request.query, docs)
        sources = [doc['id'] for doc in docs]

        log_query(request.query, answer, sources)

        return QueryResponse(answer=answer, sources=sources)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)