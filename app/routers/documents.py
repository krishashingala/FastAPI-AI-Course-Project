import os
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models import Document
from app.services.pdf_service import extract_pdf_text

router = APIRouter(prefix="/documents", tags=["Documents"])
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    content = await file.read()
    max_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(status_code=413, detail=f"File exceeds {MAX_FILE_SIZE_MB} MB limit")
    if not content.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail="Uploaded file does not look like a PDF")

    safe_name = f"{uuid4().hex}.pdf"
    path = UPLOAD_DIR / safe_name
    path.write_bytes(content)

    try:
        extracted_text = extract_pdf_text(str(path))
    except Exception as exc:
        path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail="Could not read PDF. It may be encrypted or damaged.") from exc

    doc = Document(
        filename=Path(file.filename).name,
        stored_path=str(path),
        extracted_text=extracted_text,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {
        "id": doc.id,
        "filename": doc.filename,
        "characters_extracted": len(extracted_text),
        "message": "PDF uploaded and text extracted",
    }


@router.get("")
def list_documents(db: Session = Depends(get_db)):
    docs = db.scalars(select(Document).order_by(Document.id.desc())).all()
    return [
        {"id": d.id, "filename": d.filename, "uploaded_at": d.uploaded_at.isoformat(),
         "characters_extracted": len(d.extracted_text)}
        for d in docs
    ]


@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    Path(doc.stored_path).unlink(missing_ok=True)
    db.delete(doc)
    db.commit()
    return {"message": "Document deleted", "document_id": document_id}
