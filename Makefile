# Start containers and import workflows automatically
up:
	docker compose up -d
	@echo "⏳ Waiting for n8n to start..."
	sleep 10
	@echo "🚀 Importing workflows..."
	docker exec triage-n8n n8n import:workflow --input=/data/workflows --separate --overwrite
	@echo "✅ Workflows imported. Access n8n at http://localhost:5678"

# Stop containers but keep data
down:
	docker compose down

# Reset everything (⚠️ deletes data/volumes)
reset:
	docker compose down -v

# Follow logs
logs:
	docker logs -f triage-n8n

# List containers
ps:
	docker compose ps