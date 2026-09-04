import logging
import time
from fastapi import FastAPI
from pydantic import BaseModel
from .agent import Agent
from .models import QueryRequest, QueryResponse
from .retrieval import KnowledgeBase

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("opspilot")
app = FastAPI(title="OpsPilot AI Service", version="1.0.0")
kb = KnowledgeBase()
agent = Agent(kb)


class IngestRequest(BaseModel):
    reload: bool = True


@app.get("/health")
def health():
    return {"status": "UP", "chunks": len(kb.chunks)}


@app.post("/v1/ingest")
def ingest(_: IngestRequest):
    return {"chunks": kb.reload()}


@app.post("/v1/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    started = time.perf_counter()
    result = await agent.run(request.message)
    logger.info({"event": "query.completed", "traceId": request.trace_id, "latencyMs": round((time.perf_counter()-started)*1000), "citations": len(result.citations), "guardrail": result.guardrail})
    return result

