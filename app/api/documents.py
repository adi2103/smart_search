from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas import DocumentCreate, DocumentResponse
from app.models.database import Document
from app.core.config import settings
from app.services.embedder import get_embedder
from app.services.summarizer import get_summarizer
from ..database import get_db

router = APIRouter()

@router.post("/{client_id}/documents", response_model=DocumentResponse, status_code=201)
async def create_document(
    client_id: int,
    document: DocumentCreate,
    db: Session = Depends(get_db)
):
    embedder = get_embedder(settings.embeddings_provider)
    summarizer = get_summarizer(settings.summarizer)

    embedding = embedder.encode(document.content)
    summary = summarizer.summarize(document.content, content_type="document")

    db_document = Document(
        tenant_id=settings.tenant_id,
        client_id=client_id,
        title=document.title,
        content=document.content,
        summary=summary,
        content_embedding=embedding
    )

    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    return DocumentResponse(
        id=db_document.id,
        client_id=db_document.client_id,
        title=db_document.title,
        content=db_document.content,
        summary=db_document.summary,
        created_at=db_document.created_at
    )
