.PHONY: up down test eval smoke
up:
	docker compose up --build
down:
	docker compose down
test:
	docker compose run --rm ai-service pytest -q
	docker run --rm -v "$(CURDIR)/services/api:/workspace" -w /workspace maven:3.9-eclipse-temurin-21 mvn test
eval:
	docker compose run --rm ai-service python -m app.evals
smoke:
	powershell -File scripts/smoke.ps1
