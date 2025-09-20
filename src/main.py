import logging

from fastapi import FastAPI

from src.api import documents, notes, search

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

app = FastAPI(
    title="WealthTech Smart Search API",
    description="Smart search API for client documents and meeting notes",
    version="1.0.0",
)

app.include_router(documents.router, prefix="/clients", tags=["documents"])
app.include_router(notes.router, prefix="/clients", tags=["notes"])
app.include_router(search.router, tags=["search"])


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
