import os
import signal
import time

import redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
JOB_QUEUE_NAME = os.getenv("JOB_QUEUE_NAME", "jobs")
WORKER_HEALTH_KEY = os.getenv("WORKER_HEALTH_KEY", "worker:health")

running = True

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


def handle_shutdown(signum, frame):
    global running
    print("Shutdown signal received. Stopping worker...")
    running = False


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)


def process_job(job_id):
    print(f"Processing job {job_id}", flush=True)
    r.hset(f"job:{job_id}", mapping={"status": "processing"})
    time.sleep(2)
    r.hset(f"job:{job_id}", mapping={"status": "completed"})
    print(f"Done: {job_id}", flush=True)


def main():
    r.ping()
    r.set(WORKER_HEALTH_KEY, "healthy", ex=30)

    while running:
        r.set(WORKER_HEALTH_KEY, "healthy", ex=30)
        job = r.brpop(JOB_QUEUE_NAME, timeout=5)

        if job:
            _, job_id = job
            process_job(job_id)

    print("Worker stopped cleanly.", flush=True)


if __name__ == "__main__":
    main()