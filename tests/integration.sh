#!/usr/bin/env bash

set -euo pipefail

TIMEOUT_SECONDS=60
START_TIME=$(date +%s)

echo "Waiting for frontend health..."

until curl -fs http://localhost:3000/health; do
  NOW=$(date +%s)
  ELAPSED=$((NOW - START_TIME))

  if [ "$ELAPSED" -ge "$TIMEOUT_SECONDS" ]; then
    echo "Frontend did not become healthy within ${TIMEOUT_SECONDS}s"
    docker compose logs
    exit 1
  fi

  sleep 2
done

echo "Submitting job through frontend..."

RESPONSE=$(curl -s -X POST http://localhost:3000/submit)
echo "$RESPONSE"

JOB_ID=$(echo "$RESPONSE" | python -c "import sys,json; print(json.load(sys.stdin)['job_id'])")

echo "Polling job $JOB_ID..."

START_TIME=$(date +%s)

while true; do
  STATUS_RESPONSE=$(curl -s "http://localhost:3000/status/$JOB_ID")
  echo "$STATUS_RESPONSE"

  STATUS=$(echo "$STATUS_RESPONSE" | python -c "import sys,json; print(json.load(sys.stdin)['status'])")

  if [ "$STATUS" = "completed" ]; then
    echo "Integration test passed"
    exit 0
  fi

  NOW=$(date +%s)
  ELAPSED=$((NOW - START_TIME))

  if [ "$ELAPSED" -ge "$TIMEOUT_SECONDS" ]; then
    echo "Job did not complete within ${TIMEOUT_SECONDS}s"
    docker compose logs
    exit 1
  fi

  sleep 2
done
