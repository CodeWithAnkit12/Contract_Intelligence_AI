import uuid
from pathlib import Path

from pypdf import PdfReader

from app.services.vector_store import collection
from app.utils.chunker import chunk_text

DATA_DIR = Path("data/pdfs")
DATA_DIR.mkdir(parents=True, exist_ok=True)


async def ingest_pdf(file):
    """
    Ingest a PDF file:
    1. Save PDF to disk
    2. Extract text
    3. Chunk text
    4. Store chunks in vector DB (RAG-ready)
    """
    # Generate unique document ID
    doc_id = str(uuid.uuid4())

    pdf_path = DATA_DIR / f"{doc_id}.pdf"
    txt_path = DATA_DIR / f"{doc_id}.txt"

    # Read uploaded file (async)
    content = await file.read()
    pdf_path.write_bytes(content)

    # Extract text from PDF
    reader = PdfReader(pdf_path)

    pages_text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:  # avoid None values
            pages_text.append(page_text)

    text = "\n".join(pages_text)

    # Persist raw extracted text (optional but useful for debugging / audits)
    txt_path.write_text(text, encoding="utf-8")

    # ---- RAG INGESTION ----
    chunks = chunk_text(text)

    if chunks:
        collection.add(
            documents=chunks,
            metadatas=[{"doc_id": doc_id}] * len(chunks),
            ids=[f"{doc_id}_{i}" for i in range(len(chunks))]
        )

    return {
        "doc_id": doc_id,
        "chunks_added": len(chunks),
        "status": "ingested"
    }
