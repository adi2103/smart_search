from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class DocumentCreate(BaseModel):
    title: str
    content: str

class DocumentResponse(BaseModel):
    id: int
    client_id: int
    title: str
    content: str
    summary: str
    created_at: datetime

class NoteCreate(BaseModel):
    content: str

class NoteResponse(BaseModel):
    id: int
    client_id: int
    content: str
    summary: str
    created_at: datetime

class SearchResult(BaseModel):
    id: int
    type: str
    client_id: int
    title: Optional[str] = None
    content: str
    summary: str
    created_at: datetime
    score: float

class SearchResponse(BaseModel):
    query: str
    type: Optional[str]
    results: List[SearchResult]
