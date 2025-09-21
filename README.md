# WealthTech Smart Search API

A hybrid search system for financial advisors to search client documents and meeting notes using both keyword and semantic search, with AI-powered summarization.

## 🔍 Key Features

- **Hybrid Search**: Combines PostgreSQL full-text search with vector similarity using Reciprocal Rank Fusion
- **Semantic Understanding**: sentence-transformers embeddings with pgvector for context-aware search
- **AI Summarization**: Multiple techniques - Gemini API, BART transformer, and extractive methods
- **Financial Focus**: Optimized for investment documents, meeting notes, and client communications

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone <repo-url>
cd project_20250915_2114_smart_search

# Set API key (recommended: .env file)
cp .env.example .env
nano .env  # Edit: GEMINI_API_KEY=your-actual-gemini-api-key

# Start application
docker compose up -d
```

**Alternative: Environment Variable**
```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
docker compose up -d
```

### 2. Verify Setup
```bash
curl http://localhost:8000/health  # Should return: {"status":"healthy"}
open http://localhost:8000/docs    # Interactive API documentation
```

## 🤖 Summarization Techniques

The system supports three summarization approaches, configurable via environment variable:

### Gemini API (Default)
- **Method**: Advanced language model summarization
- **Quality**: Highest - contextual, coherent summaries
- **Requirements**: API key required
- **Use Case**: Production deployments with API access

### BART Transformer
- **Method**: Local Facebook BART model
- **Quality**: High - abstractive neural summarization  
- **Requirements**: No API key, higher memory usage
- **Use Case**: Offline environments, data privacy requirements

### Extractive
- **Method**: Sentence ranking and extraction (Sumy)
- **Quality**: Good - preserves original text
- **Requirements**: Minimal resources
- **Use Case**: Fast processing, resource-constrained environments

```bash
# Switch techniques
export SUMMARIZER="gemini"      # Default
export SUMMARIZER="bart"        # Local transformer
export SUMMARIZER="extractive"  # Sentence extraction
docker compose restart api
```

## 🏗️ Architecture

```mermaid
graph TB
    Client[Client Application] --> API[FastAPI Server]
    API --> Auth[Client Validation]
    API --> Upload[Document/Note Upload]
    API --> Search[Hybrid Search Engine]
    
    Upload --> Embed[Embedding Generation]
    Upload --> Sum[Summarization]
    Embed --> Vec[Vector Storage]
    Sum --> DB[(PostgreSQL + pgvector)]
    Vec --> DB
    
    Search --> FTS[Full-Text Search]
    Search --> VSS[Vector Similarity Search]
    FTS --> DB
    VSS --> DB
    FTS --> RRF[Reciprocal Rank Fusion]
    VSS --> RRF
    RRF --> Results[Ranked Results]
    
    Sum --> Gemini[Gemini API]
    Sum --> BART[BART Model]
    Sum --> Extract[Extractive Sumy]
```

### Design Trade-offs

**Hybrid Search vs Pure Vector Search**
- ✅ Better relevance: Combines exact keyword matching with semantic similarity
- ✅ Handles both specific terms and conceptual queries
- ❌ Slightly more complex than single approach

**Multiple Summarization Options**
- ✅ Flexibility: Choose based on requirements (quality vs cost vs privacy)
- ✅ Fallback: Local methods when API unavailable
- ❌ Increased complexity and dependencies

**PostgreSQL + pgvector vs Dedicated Vector DB**
- ✅ Simpler deployment: Single database for all data
- ✅ ACID compliance: Consistent transactions
- ❌ Potentially slower than specialized vector databases at scale

## 📁 Code Structure

```
src/
├── main.py              # FastAPI application entry point
├── config.py            # Environment-based configuration
├── database.py          # SQLAlchemy database connection
├── api/                 # HTTP API layer
│   ├── documents.py     # Document upload endpoints
│   ├── notes.py         # Meeting notes endpoints
│   ├── search.py        # Hybrid search endpoints
│   └── schemas.py       # Pydantic request/response models
├── models/              # Data layer
│   └── database.py      # SQLAlchemy ORM models (Tenant, Client, Document, Note)
└── utils/               # Business logic utilities
    ├── embedder.py      # sentence-transformers embedding generation
    ├── summarizer.py    # Multi-method summarization (Gemini/BART/Extractive)
    ├── search_utils.py  # Reciprocal Rank Fusion algorithm
    └── validation.py    # Input validation helpers
```

**Key Design Decisions:**
- **Separation of Concerns**: API, models, and utilities clearly separated
- **Dependency Injection**: Configuration and services injected via FastAPI
- **Type Safety**: Pydantic schemas for all API contracts
- **Async Support**: FastAPI async handlers for better concurrency

## 📡 API Usage

### Endpoints
- `POST /clients/{id}/documents` - Upload documents with auto-summarization
- `POST /clients/{id}/notes` - Upload meeting notes with auto-summarization
- `GET /search?q=query&type=document|note` - Hybrid search with RRF ranking
- `GET /health` - Health check endpoint

### Upload Examples

**Upload Investment Document**
```bash
curl -X POST "http://localhost:8000/clients/1/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Q3 Portfolio Performance Report",
    "content": "The client portfolio achieved a 12.5% return this quarter, outperforming the S&P 500 by 2.3%. Asset allocation remains at 70% equities, 25% bonds, 5% cash. Key holdings include technology sector ETFs and dividend-focused mutual funds. Recommend rebalancing to reduce concentration risk in growth stocks."
  }'
```

**Upload Meeting Note**
```bash
curl -X POST "http://localhost:8000/clients/1/notes" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Client consultation on retirement planning. Sarah, age 52, wants to retire at 62. Current 401k balance: $485K. Contributing $22K annually. Discussed Roth conversion strategy and healthcare cost planning. Action items: review Social Security projections, increase emergency fund to 6 months expenses."
  }'
```

### Search Examples

**Unified Hybrid Search (Documents + Notes)**
```bash
# Search across all content - demonstrates D-D-D-N-N-N-D-N-N pattern
curl "http://localhost:8000/search?q=portfolio"
```

**Documents Only**
```bash
# Same query, documents filtered - consistent document ordering
curl "http://localhost:8000/search?q=portfolio&type=document"
```

**Notes Only**
```bash
# Same query, notes filtered - consistent note ordering  
curl "http://localhost:8000/search?q=portfolio&type=note"
```

### Response Comparison

**Mixed Search Results (D-D-D-N-N-N-D-N-N Pattern):**
```json
{
  "query": "portfolio",
  "results": [
    {"id": 60, "type": "document", "title": "Asset Allocation Framework", "score": 0.033},
    {"id": 57, "type": "document", "title": "Investment Strategy Guide", "score": 0.032},
    {"id": 58, "type": "document", "title": "Portfolio Analysis Report", "score": 0.032},
    {"id": 39, "type": "note", "summary": "Portfolio review meeting focused on portfolio performance analysis...", "score": 0.031},
    {"id": 40, "type": "note", "summary": "Portfolio review meeting focused on portfolio performance analysis...", "score": 0.031},
    {"id": 38, "type": "note", "summary": "Brief check-in call about financial situation including investment portfolio...", "score": 0.030},
    {"id": 59, "type": "document", "title": "Financial Planning Basics", "score": 0.016},
    {"id": 36, "type": "note", "summary": "Investment review meeting with client. Discussed investment performance...", "score": 0.015},
    {"id": 37, "type": "note", "summary": "Client consultation about investment options. Reviewed investment timeline...", "score": 0.014}
  ]
}
```

**Key Features:**
- **Unified Ranking**: Documents and notes intermixed by relevance score
- **Natural Transitions**: Content type doesn't determine position - only relevance does
- **Consistent Ordering**: Document order (60→57→58→59) and note order (39→40→38→36→37) maintained across search modes
- **Hybrid Scores**: RRF algorithm combines FTS + vector similarity for optimal relevance
```

**Search Features:**
- **Ranking**: Results ranked by relevance score (0.0-1.0)
- **Mixed Results**: Documents and notes can appear together when `type` not specified
- **Summaries**: AI-generated summaries for quick scanning
- **Full Content**: Complete original text available for detailed review

## 🧪 Testing

### Test Coverage
- **Unit Tests (17)**: Core business logic, edge cases, error handling
- **Integration Tests (11)**: End-to-end API functionality, all summarization methods
- **Total Coverage**: 28 tests covering search algorithms, AI integration, API contracts

### Running Tests
```bash
# All tests (requires running API)
docker compose exec api python -m pytest tests/ -v

# Unit tests only (~10s)
docker compose exec api python -m pytest tests/test_unit.py -v

# Integration tests (~25s)
docker compose exec api python -m pytest tests/test_integration.py -v
```

### Test Data
Integration tests use realistic financial content:
- Investment portfolio analyses
- Client meeting notes on retirement planning
- Risk assessment documents
- Asset allocation strategies

## 📚 Documentation

- **Interactive API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Format**: http://localhost:8000/redoc (ReDoc)
- **Static Documentation**: [docs/API.md](docs/API.md)
- **OpenAPI Schema**: [docs/openapi.json](docs/openapi.json)

### Auto-Update Documentation
```bash
# Manual update (requires running API)
./scripts/update-docs.sh

# Automatic updates via GitHub Actions on API changes
```

## 🆘 Troubleshooting

### Common Issues

**API Key Errors**
```bash
# Verify key is set
echo $GEMINI_API_KEY

# Use local summarization as fallback
export SUMMARIZER="bart"
docker compose restart api
```

**Container Issues**
```bash
# Restart all services
docker compose down && docker compose up -d

# Check service logs
docker compose logs api
docker compose logs db
```

**Database Connection**
```bash
# Verify database is running
docker compose ps

# Check database logs
docker compose logs db

# Reset database (removes all data)
docker compose down -v && docker compose up -d
```

**Performance Issues**
- BART model: High memory usage (~2GB), slower startup
- Gemini API: Rate limits may apply
- Vector search: Performance scales with document count
