from fastapi import APIRouter, HTTPException
from app.services.extract_service import extract_contract_fields
from pathlib import Path

router = APIRouter()

@router.post("/{document_id}")
def extract(document_id: str):
    text_path = Path(f"data/pdfs/{document_id}.txt")

    if not text_path.exists():
        raise HTTPException(status_code=404, detail="Document not found")

    text = text_path.read_text()
    extracted = extract_contract_fields(text)

    return {"document_id": document_id, "fields": extracted}
