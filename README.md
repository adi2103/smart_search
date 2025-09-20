# WealthTech Smart Search API

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Gemini API Key (Required)
```bash
# Set your Gemini API key (will be shared separately)
export GEMINI_API_KEY="your-gemini-api-key-here"
```

### 3. Start the Application
```bash
# Local development
uvicorn app.main:app --reload

# Or with Docker
docker compose up -d
```

### 4. Optional: Switch AI Methods
```bash
# Use BART (local, no API key needed)
export SUMMARIZER="bart"

# Use extractive (local, no API key needed)  
export SUMMARIZER="extractive"

# Use Gemini (default - requires API key)
export SUMMARIZER="gemini"
```

## API Endpoints

- `POST /clients/{id}/documents` - Upload documents
- `POST /clients/{id}/notes` - Upload meeting notes  
- `GET /search?q=query&type=document|note` - Hybrid search
- `GET /health` - Health check

## Architecture

- **API Layer** (`app/api/`): FastAPI endpoints and request/response schemas
- **Database** (`app/models/`): SQLAlchemy models for PostgreSQL + pgvector
- **AI Utils** (`app/utils_ai/`): Embeddings, summarization, and search utilities
- **Core** (`app/core/`): Configuration and database connection


## Testing

### Running Tests

```bash
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
