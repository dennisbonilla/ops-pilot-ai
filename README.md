# OpsPilot AI

> Project architecture website: open `docs/index.html` locally or enable GitHub Pages using the included workflow.

A full-stack portfolio lab: an operations copilot that answers questions from runbooks with RAG, cites its sources, and proposes safe tool actions. Write actions require human approval.

## What it demonstrates

- **TypeScript/React:** conversational UI with evidence, traces, and approvals.
- **Java/Spring Boot:** public API, validation, auditing, and service orchestration.
- **Python/FastAPI:** ingestion, hybrid retrieval, agent workflow, guardrails, and evaluations.
- **AI engineering:** RAG, tool calling, MCP, cited answers, evals, and observability.
- **Production readiness:** containers, health checks, structured logs, tests, and CI.

## Architecture

```text
React :3000 -> Java API :8080 -> Python AI :8000
                    |              |-- persistent local vector store
                    |              |-- interchangeable LLM provider
                    |              `-- tools + MCP server
                    `-- audit trail and approval policy
```

Demo mode requires no API keys. It uses a deterministic model so the complete workflow can be demonstrated reliably. To use an OpenAI-compatible provider, configure `LLM_BASE_URL`, `LLM_API_KEY`, and `LLM_MODEL`.

## Quick start

Requirement: Docker Desktop.

```bash
docker compose up --build
```

Open http://localhost:3000 and ask: `What should I do when the API has high latency?`

You can also run `make test`, `make eval`, and `make smoke`.

## Product decisions

1. Answers must include retrieved evidence. The system abstains when evidence is insufficient.
2. Read-only tools may run automatically. Write tools generate a pending proposal.
3. Every request includes a `traceId`, latency, retrieved documents, and a safety decision.
4. A versioned dataset measures factual accuracy, groundedness, citation coverage, and tool selection.

## Main API

- `POST /api/chat`: question, answer, citations, and optional action.
- `POST /api/actions/{id}/approve`: approves a pending action.
- `GET /api/health`: aggregated service health.
- `GET /health`, `POST /v1/query`, `POST /v1/ingest`: AI service operations.

## Three-minute interview demo

1. Ask a question covered by the runbooks and highlight its citations.
2. Ask `create an incident for critical latency`: the agent proposes the action but does not execute it.
3. Approve the action and show the audit event.
4. Show `evals/dataset.jsonl` and run the quality gate.
5. Explain how the LLM provider can change without modifying product contracts.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/PORTFOLIO.md](docs/PORTFOLIO.md) for the technical narrative and suggested next steps.
