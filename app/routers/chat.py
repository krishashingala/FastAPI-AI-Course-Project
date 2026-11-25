from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models import Document
from app.schemas import ChatRequest, ChatResponse
from app.services.retrieval_service import retrieve_excerpt

router = APIRouter(tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    if payload.document_id is not None:
        doc = db.get(Document, payload.document_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        excerpt = retrieve_excerpt(doc.extracted_text, payload.question)
        if not excerpt:
            answer = "No readable text was found in this PDF. It may be scanned; OCR is not included."
        else:
            answer = (
                "Relevant text extracted from your document:\n\n"
                + excerpt
                + "\n\nNote: This starter project retrieves excerpts; it does not generate an LLM answer."
            )
        return ChatResponse(
            question=payload.question,
            answer=answer,
            document_id=doc.id,
            note="Educational keyword-retrieval demo. Add embeddings, a vector database, and an LLM for full RAG."
        )

    doc = db.scalars(select(Document).order_by(Document.id.desc())).first()
    if not doc:
        raise HTTPException(status_code=400, detail="Upload a PDF first or provide a document_id")
    excerpt = retrieve_excerpt(doc.extracted_text, payload.question)
    answer = excerpt or "No matching text found in the latest document."
    return ChatResponse(
        question=payload.question,
        answer=answer,
        document_id=doc.id,
        note="Starter retrieval only; no LLM is connected."
    )
