import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.api.schemas import SearchResponse, SearchResult
from src.config import settings
from src.models.database import Document, MeetingNote
from src.utils.embedder import get_embedder
from src.utils.search_utils import reciprocal_rank_fusion
from src.utils.validation import validate_search_query

from ..database import get_db

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/search", response_model=SearchResponse)
async def search(
    q: str = Query(..., description="Search query"),
    type: Optional[str] = Query(None, description="Filter by type: document or note"),
    db: Session = Depends(get_db),
):
    try:
        # Validate search query
        validate_search_query(q)

        # Validate type parameter
        if type and type not in ["document", "note"]:
            raise HTTPException(status_code=400, detail="Type must be 'document' or 'note'")

        # Get embedder with error handling
        try:
            embedder = get_embedder(settings.embeddings_provider)
            query_embedding = embedder.encode(q)
        except Exception as e:
            logger.error(f"Embedding generation failed for search: {e}")
            raise HTTPException(status_code=500, detail="Failed to process search query")

        all_fts_results = []
        all_vector_results = []

        # Search documents
        if not type or type == "document":
            try:
                # FTS search
                fts_query = text(
                    """
                    SELECT id, ts_rank(content_tsv, plainto_tsquery(:query)) as score
                    FROM documents
                    WHERE tenant_id = :tenant_id AND content_tsv @@ plainto_tsquery(:query)
                    ORDER BY score DESC LIMIT 50
                """
                )
                fts_results = db.execute(fts_query, {"query": q, "tenant_id": settings.tenant_id}).fetchall()

                # Vector search using SQLAlchemy ORM
                vector_results = (
                    db.query(Document.id, Document.content_embedding.l2_distance(query_embedding).label("distance"))
                    .filter(Document.tenant_id == settings.tenant_id)
                    .order_by("distance")
                    .limit(50)
                    .all()
                )

                # Add to unified results with type prefix
                all_fts_results.extend([("doc_" + str(r.id), r.score) for r in fts_results])
                all_vector_results.extend([("doc_" + str(r.id), 1 - r.distance) for r in vector_results])

            except SQLAlchemyError as e:
                logger.error(f"Database error searching documents: {e}")
                raise HTTPException(status_code=500, detail="Error searching documents")

        # Search notes
        if not type or type == "note":
            try:
                # FTS search
                fts_query = text(
                    """
                    SELECT id, ts_rank(content_tsv, plainto_tsquery(:query)) as score
                    FROM meeting_notes
                    WHERE tenant_id = :tenant_id AND content_tsv @@ plainto_tsquery(:query)
                    ORDER BY score DESC LIMIT 50
                """
                )
                fts_results = db.execute(fts_query, {"query": q, "tenant_id": settings.tenant_id}).fetchall()

                # Vector search using SQLAlchemy ORM
                vector_results = (
                    db.query(
                        MeetingNote.id, MeetingNote.content_embedding.l2_distance(query_embedding).label("distance")
                    )
                    .filter(MeetingNote.tenant_id == settings.tenant_id)
                    .order_by("distance")
                    .limit(50)
                    .all()
                )

                # Add to unified results with type prefix
                all_fts_results.extend([("note_" + str(r.id), r.score) for r in fts_results])
                all_vector_results.extend([("note_" + str(r.id), 1 - r.distance) for r in vector_results])

            except SQLAlchemyError as e:
                logger.error(f"Database error searching notes: {e}")
                raise HTTPException(status_code=500, detail="Error searching notes")

        # Unified RRF ranking across all results
        merged = reciprocal_rank_fusion(all_fts_results, all_vector_results)

        # Get top results and fetch from database
        results = []
        for item_id, score in merged[:20]:  # Top 20 results
            if item_id.startswith("doc_"):
                doc_id = int(item_id[4:])  # Remove "doc_" prefix
                doc = db.query(Document).filter(Document.id == doc_id).first()
                if doc:
                    results.append(
                        SearchResult(
                            id=doc.id,
                            type="document",
                            client_id=doc.client_id,
                            title=doc.title,
                            content=doc.content,
                            summary=doc.summary,
                            created_at=doc.created_at,
                            score=score,
                        )
                    )
            elif item_id.startswith("note_"):
                note_id = int(item_id[5:])  # Remove "note_" prefix
                note = db.query(MeetingNote).filter(MeetingNote.id == note_id).first()
                if note:
                    results.append(
                        SearchResult(
                            id=note.id,
                            type="note",
                            client_id=note.client_id,
                            title=None,
                            content=note.content,
                            summary=note.summary,
                            created_at=note.created_at,
                            score=score,
                        )
                    )

        return SearchResponse(query=q, type=type, results=results)

    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in search: {e}")
        raise HTTPException(status_code=500, detail="Search operation failed")
