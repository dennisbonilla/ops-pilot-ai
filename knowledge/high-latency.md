# Runbook: high API latency

When p95 latency exceeds 800 ms for five minutes, first check CPU saturation, connection-pool usage, and dependency latency. Compare the timing with the most recent deployment.

If the error rate also exceeds 5%, create a SEV-2 incident and notify the Platform team. A rollback requires incident commander approval. Never restart production as the first response.
