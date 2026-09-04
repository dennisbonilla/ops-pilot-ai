# Runbook: database connections

When connection-pool usage exceeds 85% for ten minutes, inspect slow queries and open transactions. Reduce nonessential traffic before increasing the pool size.

Do not terminate sessions or modify production parameters without approval. Record every action in the active incident.
