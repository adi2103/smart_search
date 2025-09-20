from fastapi import FastAPI
from src.api import documents, notes, search
from src.config import settings
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="WealthTech Smart Search API",
    description="Smart search API for client documents and meeting notes",
    version="1.0.0"
)

src.include_router(documents.router, prefix="/clients", tags=["documents"])
src.include_router(notes.router, prefix="/clients", tags=["notes"])
src.include_router(search.router, tags=["search"])

@src.get("/health")
async def health_check():
    return {"status": "healthy"}
