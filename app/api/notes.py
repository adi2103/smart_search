from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.schemas import NoteCreate, NoteResponse
from app.models.database import MeetingNote
from app.core.config import settings
from app.services.embedder import get_embedder
from app.services.summarizer import get_summarizer
from ..database import get_db

router = APIRouter()

@router.post("/{client_id}/notes", response_model=NoteResponse, status_code=201)
async def create_note(
    client_id: int,
    note: NoteCreate,
    db: Session = Depends(get_db)
):
    embedder = get_embedder(settings.embeddings_provider)
    summarizer = get_summarizer(settings.summarizer)

    # Generate embedding and summary
    embedding = embedder.encode(note.content)
    summary = summarizer.summarize(note.content, content_type="note")

    # Create note
    db_note = MeetingNote(
        tenant_id=settings.tenant_id,
        client_id=client_id,
        content=note.content,
        summary=summary,
        content_embedding=embedding
    )

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return NoteResponse(
        id=db_note.id,
        client_id=db_note.client_id,
        content=db_note.content,
        summary=db_note.summary,
        created_at=db_note.created_at
    )
