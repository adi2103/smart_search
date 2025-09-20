from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class DocumentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500, description="Document title")
    content: str = Field(..., min_length=1, max_length=50000, description="Document content")

    @validator("title")
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @validator("content")
    def content_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Content cannot be empty")
        return v.strip()


class DocumentResponse(BaseModel):
    id: int
    client_id: int
    title: str
    content: str
    summary: str
    created_at: datetime


class NoteCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=50000, description="Note content")

    @validator("content")
    def content_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Content cannot be empty")
        return v.strip()


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
