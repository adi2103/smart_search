from fastapi import FastAPI
from app.api import documents, notes, search
from app.core.config import settings

app = FastAPI(
    title="WealthTech Smart Search API",
    description="Smart search API for client documents and meeting notes",
    version="1.0.0"
)

app.include_router(documents.router, prefix="/clients", tags=["documents"])
app.include_router(notes.router, prefix="/clients", tags=["notes"])
app.include_router(search.router, tags=["search"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
