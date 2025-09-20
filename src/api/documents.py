from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.api.schemas import DocumentCreate, DocumentResponse
from src.models.database import Document
from src.config import settings
from src.utils.embedder import get_embedder
from src.utils.summarizer import get_summarizer
from src.utils.validation import validate_client_exists, validate_content_length
from ..database import get_db
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/{client_id}/documents", response_model=DocumentResponse, status_code=201)
async def create_document(
    client_id: int,
    document: DocumentCreate,
    db: Session = Depends(get_db)
):
    try:
        # Validate client exists and belongs to tenant
        validate_client_exists(client_id, db)

        # Validate content length
        validate_content_length(document.content)

        # Get services
        embedder = get_embedder(settings.embeddings_provider)
        summarizer = get_summarizer(settings.summarizer)

        # Generate embedding with error handling
        try:
            embedding = embedder.encode(document.content)
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate document embedding"
            )

        # Generate summary with error handling (has built-in fallback)
        try:
            summary = summarizer.summarize(document.content, content_type="document")
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate document summary"
            )

        # Create document
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

    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error in create_document: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )
    except Exception as e:
        logger.error(f"Unexpected error in create_document: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
