from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest
import time
import random
import logging

# --------------------
# ЛОГИРОВАНИЕ
# --------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --------------------
# ПРИЛОЖЕНИЕ
# --------------------
app = FastAPI(title="DevOps Practice Service")

# --------------------
# МЕТРИКИ
# --------------------
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests"
)

# --------------------
# ENDPOINTS
# --------------------
@app.get("/")
def root():
    REQUEST_COUNT.inc()
    logger.info("Root endpoint called")
    return {"message": "Hello from DevOps service"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/error")
def error():
    REQUEST_COUNT.inc()
    logger.error("Error endpoint called")
    return Response(status_code=500)

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )
