#!/usr/bin/env bash
set -euo pipefail

echo "=== AlphaEdge Setup ==="

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed."; exit 1; }
command -v docker compose >/dev/null 2>&1 || { echo "Docker Compose V2 is required."; exit 1; }

# Copy env file if not present
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from .env.example — please edit it with your settings."
fi

# Build and start services
docker compose up -d --build

# Wait for DB to be ready
echo "Waiting for database..."
sleep 5

# Run migrations
docker compose exec backend alembic upgrade head

# Seed data
docker compose exec backend python /app/../scripts/seed.py

echo ""
echo "=== Setup Complete ==="
echo "Backend API:  http://localhost:8000"
echo "API Docs:     http://localhost:8000/docs"
echo "Frontend:     http://localhost:3000"
echo "Demo login:   demo@alphaedge.local / demo1234"
