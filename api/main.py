from fastapi import FastAPI, HTTPException
import os
import redis
import uuid

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
JOB_QUEUE_NAME = os.getenv("JOB_QUEUE_NAME", "jobs")

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


@app.get("/health")
def health():
    try:
        r.ping()
        return {"status": "healthy"}
    except redis.RedisError:
        raise HTTPException(status_code=503, detail="Redis unavailable")


@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())
    r.hset(f"job:{job_id}", mapping={"status": "queued"})
    r.lpush(JOB_QUEUE_NAME, job_id)
    return {"job_id": job_id, "status": "queued"}


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")

    if not status:
        raise HTTPException(status_code=404, detail="Job not found")

    return {"job_id": job_id, "status": status}
