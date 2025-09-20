from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from app.schemas.schemas import SearchResponse, SearchResult
from app.models.database import Document, MeetingNote
from app.core.config import settings
from app.services.embedder import get_embedder
from app.services.search import reciprocal_rank_fusion
from app.utils.validation import validate_search_query
from ..database import get_db
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/search", response_model=SearchResponse)
async def search(
    q: str = Query(..., description="Search query"),
    type: Optional[str] = Query(None, description="Filter by type: document or note"),
    db: Session = Depends(get_db)
):
    try:
        # Validate search query
        validate_search_query(q)

        # Validate type parameter
        if type and type not in ["document", "note"]:
            raise HTTPException(
                status_code=400,
                detail="Type must be 'document' or 'note'"
            )

        # Get embedder with error handling
        try:
            embedder = get_embedder(settings.embeddings_provider)
            query_embedding = embedder.encode(q)
        except Exception as e:
            logger.error(f"Embedding generation failed for search: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to process search query"
            )

        results = []

        # Search documents
        if not type or type == "document":
            try:
                # FTS search
                fts_query = text("""
                    SELECT id, ts_rank(content_tsv, plainto_tsquery(:query)) as score
                    FROM documents
                    WHERE tenant_id = :tenant_id AND content_tsv @@ plainto_tsquery(:query)
                    ORDER BY score DESC LIMIT 50
                """)
                fts_results = db.execute(fts_query, {"query": q, "tenant_id": settings.tenant_id}).fetchall()

                # Vector search using SQLAlchemy ORM
                vector_results = db.query(
                    Document.id,
                    Document.content_embedding.l2_distance(query_embedding).label('distance')
                ).filter(
                    Document.tenant_id == settings.tenant_id
                ).order_by('distance').limit(50).all()

                # Merge with RRF
                fts_list = [(r.id, r.score) for r in fts_results]
                vector_list = [(r.id, 1-r.distance) for r in vector_results]
                merged = reciprocal_rank_fusion(fts_list, vector_list)

                # Get top documents
                doc_ids = [doc_id for doc_id, _ in merged[:10]]
                if doc_ids:
                    docs = db.query(Document).filter(Document.id.in_(doc_ids)).all()
                    for doc in docs:
                        score = next(score for doc_id, score in merged if doc_id == doc.id)
                        results.append(SearchResult(
                            id=doc.id,
                            type="document",
                            client_id=doc.client_id,
                            title=doc.title,
                            content=doc.content,
                            summary=doc.summary,
                            created_at=doc.created_at,
                            score=score
                        ))

            except SQLAlchemyError as e:
                logger.error(f"Database error searching documents: {e}")
                raise HTTPException(
                    status_code=500,
                    detail="Error searching documents"
                )

        # Search notes
        if not type or type == "note":
            try:
                # FTS search
                fts_query = text("""
                    SELECT id, ts_rank(content_tsv, plainto_tsquery(:query)) as score
                    FROM meeting_notes
                    WHERE tenant_id = :tenant_id AND content_tsv @@ plainto_tsquery(:query)
                    ORDER BY score DESC LIMIT 50
                """)
                fts_results = db.execute(fts_query, {"query": q, "tenant_id": settings.tenant_id}).fetchall()

                # Vector search using SQLAlchemy ORM
                vector_results = db.query(
                    MeetingNote.id,
                    MeetingNote.content_embedding.l2_distance(query_embedding).label('distance')
                ).filter(
                    MeetingNote.tenant_id == settings.tenant_id
                ).order_by('distance').limit(50).all()

                # Merge with RRF
                fts_list = [(r.id, r.score) for r in fts_results]
                vector_list = [(r.id, 1-r.distance) for r in vector_results]
                merged = reciprocal_rank_fusion(fts_list, vector_list)

                # Get top notes
                note_ids = [note_id for note_id, _ in merged[:10]]
                if note_ids:
                    notes = db.query(MeetingNote).filter(MeetingNote.id.in_(note_ids)).all()
                    for note in notes:
                        score = next(score for note_id, score in merged if note_id == note.id)
                        results.append(SearchResult(
                            id=note.id,
                            type="note",
                            client_id=note.client_id,
                            title=None,
                            content=note.content,
                            summary=note.summary,
                            created_at=note.created_at,
                            score=score
                        ))

            except SQLAlchemyError as e:
                logger.error(f"Database error searching notes: {e}")
                raise HTTPException(
                    status_code=500,
                    detail="Error searching notes"
                )

        # Results are already in RRF-optimized order, no additional sorting needed
        return SearchResponse(
            query=q,
            type=type,
            results=results
        )

    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in search: {e}")
        raise HTTPException(
            status_code=500,
            detail="Search operation failed"
        )
