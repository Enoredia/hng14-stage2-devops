# FIXES.md

| File | Line | Issue | Fix |
|---|---:|---|---|
| api/main.py | 8 | Redis host was hardcoded to localhost, which fails inside Docker because localhost refers to the API container, not the Redis container. | Replaced hardcoded Redis connection with REDIS_HOST and REDIS_PORT environment variables. |
| api/main.py | 8 | Redis values required manual decode using status.decode(), which adds unnecessary handling and can cause inconsistent response behavior. | Added decode_responses=True to the Redis client and removed manual decoding. |
| api/main.py | 11 | Queue name was hardcoded as "job", making configuration inflexible across local, Docker, and CI environments. | Added JOB_QUEUE_NAME environment variable with a default value. |
| api/main.py | N/A | No health endpoint existed for container healthchecks and service dependency checks. | Added GET /health endpoint that checks Redis connectivity with r.ping(). |
| api/main.py | 19 | Missing jobs returned {"error": "not found"} with HTTP 200, which is misleading. | Changed missing job response to raise HTTP 404 using FastAPI HTTPException. |
| api/requirements.txt | 1-3 | Dependencies were not version-pinned, leading to non-reproducible builds across environments and potential CI/CD failures. | Added explicit version pinning for all dependencies and included uvicorn[standard] for production readiness. |
| worker/worker.py | 6 | Redis host was hardcoded to localhost, which fails inside Docker because localhost refers to the worker container, not the Redis container. | Replaced hardcoded Redis connection with REDIS_HOST and REDIS_PORT environment variables. |
| worker/worker.py | 6 | Redis client did not use decode_responses=True, requiring manual byte decoding with job_id.decode(). | Added decode_responses=True to the Redis client and removed manual decoding. |
| worker/worker.py | 13 | Queue name was hardcoded as "job", making the API and worker difficult to configure consistently across local, Docker, and CI environments. | Added JOB_QUEUE_NAME environment variable with a default value shared by the API and worker. |
| worker/worker.py | 4 | signal was imported but no shutdown signal handling was implemented. | Added SIGTERM and SIGINT handlers so the worker can shut down cleanly in Docker and CI. |
| worker/worker.py | N/A | Worker had no health indicator for Docker healthchecks. | Added a Redis-backed worker health key that is refreshed while the worker is running. |
| worker/worker.py | 9 | Job status moved directly from queued to completed, giving no visibility that a job was actively being processed. | Added an intermediate processing status before marking the job as completed. |
| frontend/app.js | 6 | API URL was hardcoded to http://localhost:8000, which fails inside Docker because localhost refers to the frontend container, not the API container. | Replaced with API_URL environment variable and defaulted to http://api:8000. |
| frontend/app.js | 6 | API URL was not configurable across environments (local, Docker, CI). | Introduced API_URL environment variable for flexibility. |
| frontend/app.js | N/A | No health endpoint existed for Docker healthchecks and dependency readiness. | Added GET /health endpoint returning a healthy status. |
| frontend/app.js | 12 | Errors were swallowed without logging, making debugging difficult. | Added console.error logging for failed API calls. |
| frontend/app.js | 18 | Application port was hardcoded to 3000, limiting flexibility. | Replaced with PORT environment variable with default value. |
| frontend/package.json | 7-10 | Dependency versions used caret ranges, which can lead to inconsistent installs across local, Docker, and CI environments. | Pinned dependency versions for reproducible builds. |
| frontend/package.json | 4 | No lint script existed, but the CI pipeline requires JavaScript linting with ESLint. | Added a lint script using ESLint. |
| frontend/package.json | N/A | ESLint was missing from devDependencies, so JavaScript linting could not run in CI. | Added ESLint as a development dependency. |
| worker/requirements.txt | 1 | Dependency entry was incorrectly written as "redis(venv)", which is invalid syntax and prevents pip from installing the package. | Replaced with a properly formatted and version-pinned dependency "redis==5.0.1". |
