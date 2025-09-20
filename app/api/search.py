from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from app.schemas.schemas import SearchResponse, SearchResult
from app.models.database import Document, MeetingNote
from app.core.config import settings
from app.services.embedder import get_embedder
from app.services.search import reciprocal_rank_fusion
from ..database import get_db

router = APIRouter()

@router.get("/search", response_model=SearchResponse)
async def search(
    q: str = Query(..., description="Search query"),
    type: Optional[str] = Query(None, description="Filter by type: document or note"),
    db: Session = Depends(get_db)
):
    embedder = get_embedder(settings.embeddings_provider)
    query_embedding = embedder.encode(q)  # Keep as numpy array for SQLAlchemy ORM

    results = []

    # Search documents
    if not type or type == "document":
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
        vector_list = [(r.id, 1-r.distance) for r in vector_results]  # Convert distance to similarity
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

    # Search notes
    if not type or type == "note":
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

    # Results are already in RRF-optimized order, no additional sorting needed
    return SearchResponse(
        query=q,
        type=type,
        results=results
    )
