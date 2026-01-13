from fastapi import APIRouter, HTTPException
from pathlib import Path
from app.services.audit_service import audit_contract

router = APIRouter()

@router.post("/{document_id}")
def audit(document_id: str):
    path = Path(f"data/pdfs/{document_id}.txt")
    if not path.exists():
        raise HTTPException(404, "Document not found")

    text = path.read_text()
    return audit_contract(text)
