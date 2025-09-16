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
    query_embedding = embedder.encode(q)
    
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
        
        # Vector search
        vector_query = text("""
            SELECT id, (content_embedding <-> :embedding) as distance
            FROM documents 
            WHERE tenant_id = :tenant_id
            ORDER BY distance LIMIT 50
        """)
        vector_results = db.execute(vector_query, {"embedding": query_embedding, "tenant_id": settings.tenant_id}).fetchall()
        
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
    
    # Search notes (similar logic)
    if not type or type == "note":
        # Similar implementation for notes...
        pass
    
    # Sort by score
    results.sort(key=lambda x: x.score, reverse=True)
    
    return SearchResponse(
        query=q,
        type=type,
        results=results
    )
