FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim AS runtime

WORKDIR /app

ENV PATH=/home/appuser/.local/bin:$PATH

RUN groupadd -r appgroup && useradd -r -g appgroup -m appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY . .

RUN chown -R appuser:appgroup /app /home/appuser/.local

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --retries=5 CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
