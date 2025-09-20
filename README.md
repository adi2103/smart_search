# WealthTech Smart Search API

## Current Status: MVP Core Complete (~75%)

### ✅ Implemented (13 files, 30 symbols)
- **FastAPI Structure**: Complete app architecture with routers
- **Database Models**: SQLAlchemy models (Tenant, Client, Document, MeetingNote) 
- **API Endpoints**: All 3 required endpoints implemented
  - `POST /clients/{id}/documents`
  - `POST /clients/{id}/notes`
  - `GET /search?q=...&type=document|note`
- **Core Services**: Embedder (sentence-transformers), Summarizer (Sumy), Search (RRF)
- **Schemas**: Pydantic request/response models
- **Docker Setup**: Compose file with PostgreSQL + pgvector

### ⚠️ Current Issues
- **API Container**: Crashed due to import path issues
- **Database**: No schema initialization (tables don't exist)
- **Missing**: Database migrations, error handling, comprehensive tests

### 🔧 Services Status
- **Database**: ✅ Running (PostgreSQL + pgvector on port 5432)
- **API**: ❌ Not running (needs import fixes and DB init)

### 📊 Development Progress
- **Design Document**: ✅ Complete (WealthTech_Smart_Search_Design.md)
- **Core Implementation**: ✅ 75% done
- **Testing**: ❌ Not started
- **Deployment**: 🔄 Partially working (DB up, API down)

### 🚧 Immediate Blockers
1. Fix Python import paths in API modules
2. Create database initialization script (CREATE EXTENSION pgvector, CREATE TABLES)
3. Add proper error handling for missing database connections
4. Restart API container after fixes

### 🎯 Next Steps to Complete MVP
1. **Database Init**: Create schema initialization script
2. **Fix Imports**: Resolve module import issues in FastAPI app
3. **API Testing**: Verify all endpoints work with curl/Postman
4. **Integration Tests**: Test full document upload → search workflow
5. **Error Handling**: Add proper validation and error responses

### 🏗️ Architecture Overview
```
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── core/config.py       # Settings and configuration
│   ├── models/database.py   # SQLAlchemy models
│   ├── schemas/schemas.py   # Pydantic schemas
│   ├── api/                 # API route handlers
│   │   ├── documents.py     # Document upload endpoint
│   │   ├── notes.py         # Notes upload endpoint
│   │   └── search.py        # Hybrid search endpoint
│   └── services/            # Core business logic
│       ├── embedder.py      # Text embedding generation
│       ├── summarizer.py    # Text summarization
│       └── search.py        # Hybrid search with RRF
├── docker-compose.yml       # Container orchestration
├── Dockerfile              # API container definition
└── requirements.txt        # Python dependencies
```

### 🔍 Tech Stack
- **API**: FastAPI + Pydantic + SQLAlchemy
- **Database**: PostgreSQL 15+ with pgvector extension
- **Embeddings**: sentence-transformers (local, no API costs)
- **Summarization**: Sumy (extractive, deterministic)
- **Search**: Hybrid (FTS + vector) with Reciprocal Rank Fusion
- **Deployment**: Docker Compose for local development

### 📝 Design Specifications
See `WealthTech_Smart_Search_Design.md` for complete architecture details, API specifications, and implementation decisions.

---
**Estimated Time to Complete**: 2-3 hours remaining for fully functional MVP
**Last Updated**: 2025-09-16T21:58:43+01:00


## Installation

### Simple Setup
```bash
# Install all dependencies (includes all AI methods)
pip install -r requirements.txt

# Set your Gemini API key
export GEMINI_API_KEY="your-api-key"

# Optional: Choose summarization method (default: gemini)
export SUMMARIZER="gemini"  # or "extractive" or "bart"
```

## Docker Deployment

### Quick Start
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your GEMINI_API_KEY
nano .env

# Start the application (all AI methods included)
docker compose up -d
```

### Switch AI Methods
```bash
# Use Gemini (default - requires API key)
echo "SUMMARIZER=gemini" >> .env

# Use BART (local, no API key needed)
echo "SUMMARIZER=bart" >> .env

# Use extractive (local, no API key needed)
echo "SUMMARIZER=extractive" >> .env

# Restart to apply changes
docker compose restart api
```


## Testing

### Test Structure
- `tests/test_unit.py` - Unit tests for core business logic and regression prevention
- `tests/test_integration.py` - Integration tests for complete API functionality

### Running Tests

```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run unit tests (fast, ~14s)
python -m pytest tests/test_unit.py -v

# Run integration tests (requires API running, ~90s)
python -m pytest tests/test_integration.py -v

# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/test_unit.py --cov=app --cov-report=term-missing
```

### Test Coverage
- **Unit Tests**: Core business logic, edge cases, regression prevention
- **Integration Tests**: Complete API functionality via HTTP requests
- **Combined**: Comprehensive system validation
