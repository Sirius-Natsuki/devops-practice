from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
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

ERROR_COUNT = Counter(
    "http_requests_errors_total",
    "Total HTTP requests that returned errors"
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
    ERROR_COUNT.inc()
    logger.error("Error endpoint called")
    return Response(status_code=500)

@app.get("/simulate")
def simulate():
    """Эндпоинт для тестирования нагрузки и ошибок"""
    REQUEST_COUNT.inc()
    delay = random.uniform(0.1, 2.0)
    time.sleep(delay)
    if random.random() < 0.2:
        ERROR_COUNT.inc()
        logger.error("Simulated error!")
        return Response(status_code=500)
    logger.info(f"Simulated delay {delay:.2f}s")
    return {"status": "ok", "delay": delay}

@app.get("/metrics")
def metrics():
    """Prometheus endpoint"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
