import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.api.schemas import NoteCreate, NoteResponse
from src.config import settings
from src.models.database import MeetingNote
from src.utils.embedder import get_embedder
from src.utils.summarizer import get_summarizer
from src.utils.validation import validate_client_exists, validate_content_length

from ..database import get_db

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/{client_id}/notes", response_model=NoteResponse, status_code=201)
async def create_note(client_id: int, note: NoteCreate, db: Session = Depends(get_db)):
    try:
        # Validate client exists and belongs to tenant
        validate_client_exists(client_id, db)

        # Validate content length
        validate_content_length(note.content)

        # Get services
        embedder = get_embedder(settings.embeddings_provider)
        summarizer = get_summarizer(settings.summarizer)

        # Generate embedding with error handling
        try:
            embedding = embedder.encode(note.content)
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise HTTPException(status_code=500, detail="Failed to generate note embedding")

        # Generate summary with error handling (has built-in fallback)
        try:
            summary = summarizer.summarize(note.content, content_type="note")
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            raise HTTPException(status_code=500, detail="Failed to generate note summary")

        # Create note
        db_note = MeetingNote(
            tenant_id=settings.tenant_id,
            client_id=client_id,
            content=note.content,
            summary=summary,
            content_embedding=embedding,
        )

        db.add(db_note)
        db.commit()
        db.refresh(db_note)

        return NoteResponse(
            id=db_note.id,
            client_id=db_note.client_id,
            content=db_note.content,
            summary=db_note.summary,
            created_at=db_note.created_at,
        )

    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error in create_note: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database operation failed")
    except Exception as e:
        logger.error(f"Unexpected error in create_note: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
