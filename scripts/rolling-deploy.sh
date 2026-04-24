#!/usr/bin/env bash

set -e

echo "Starting scripted rolling deployment..."

cp .env.example .env

docker compose up --build -d redis api worker frontend-new || true

echo "Waiting for new frontend container health check..."

for i in {1..30}; do
  if curl -fs http://localhost:3000/health; then
    echo "New container passed health check"
    echo "Rolling deployment completed successfully"
    exit 0
  fi

  echo "Health check not ready yet..."
  sleep 2
done

echo "Health check failed after 60 seconds. Aborting deployment."
exit 1
