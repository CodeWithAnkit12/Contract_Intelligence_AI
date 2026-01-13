from fastapi import APIRouter, UploadFile, File
from app.services.pdf_service import ingest_pdf

router = APIRouter()

@router.post("/")
async def ingest(files: list[UploadFile] = File(...)):
    doc_ids = []
    for file in files:
        doc_id = await ingest_pdf(file)
        doc_ids.append(doc_id)
    return {"document_ids": doc_ids}
