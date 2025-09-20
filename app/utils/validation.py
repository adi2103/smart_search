from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.database import Client
from app.core.config import settings

def validate_client_exists(client_id: int, db: Session) -> Client:
    """Validate client exists and belongs to tenant_id=1"""
    client = db.query(Client).filter(
        Client.id == client_id,
        Client.tenant_id == settings.tenant_id
    ).first()
    
    if not client:
        raise HTTPException(
            status_code=404, 
            detail=f"Client {client_id} not found"
        )
    
    return client

def validate_content_length(content: str, max_length: int = 50000) -> None:
    """Validate content length limits"""
    if len(content) > max_length:
        raise HTTPException(
            status_code=400,
            detail=f"Content too long. Maximum {max_length} characters allowed"
        )

def validate_search_query(query: str) -> None:
    """Validate search query parameters"""
    if not query or not query.strip():
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty"
        )
    
    if len(query) > 1000:
        raise HTTPException(
            status_code=400,
            detail="Search query too long. Maximum 1000 characters allowed"
        )
