from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    message: str = Field(min_length=2, max_length=2000)
    session_id: str = Field(default="anonymous", max_length=100)
    trace_id: str


class Citation(BaseModel):
    source: str
    excerpt: str
    score: float


class ToolProposal(BaseModel):
    name: str
    arguments: dict[str, str]
    risk: str = "write"


class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
    confidence: float
    tool_proposal: ToolProposal | None = None
    guardrail: str = "passed"

