$ErrorActionPreference = "Stop"
$health = Invoke-RestMethod http://localhost:8080/api/health
if ($health.status -ne "UP") { throw "API is not healthy" }
$body = @{sessionId="smoke"; message="What should I do when the API has high latency?"} | ConvertTo-Json
$result = Invoke-RestMethod -Method Post -Uri http://localhost:8080/api/chat -ContentType "application/json" -Body $body
if (-not $result.citations) { throw "Expected citations" }
Write-Host "Smoke test OK - traceId=$($result.traceId)"
