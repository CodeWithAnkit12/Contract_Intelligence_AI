from fastapi import APIRouter
from prometheus_client import Counter, generate_latest

router = APIRouter()

REQUEST_COUNT = Counter("requests_total", "Total API requests")

@router.get("/healthz")
def health():
    REQUEST_COUNT.inc()
    return {"status": "ok"}

@router.get("/metrics")
def metrics():
    return generate_latest()
