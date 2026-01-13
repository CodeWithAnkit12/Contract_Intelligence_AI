from fastapi import FastAPI
from app.api import ingest, extract, ask, audit, health
from app.api import ui

app = FastAPI(
    title="Contract Intelligence API",
    description="AI-powered contract analysis with RAG, audit & streaming",
    version="1.0.0"
)

app.include_router(health.router)
app.include_router(ingest.router, prefix="/ingest", tags=["Ingest"])
app.include_router(extract.router, prefix="/extract", tags=["Extract"])
app.include_router(ask.router, prefix="/ask", tags=["Ask"])
app.include_router(audit.router, prefix="/audit", tags=["Audit"])
app.include_router(ui.router)
