
# WealthTech Smart Search API – Architecture & Design (Multi-tenant Ready, Single-Tenant MVP)

## 1. Overview
This document presents the architecture and design for a **Smart Search API** in a WealthTech advisor platform. The API enables advisors to search through client documents and meeting notes using **keyword search**, **semantic search**, and **AI-powered summaries**.

Core principles and MVP scope:
- **Hybrid Search**: Combine PostgreSQL full-text search with semantic embeddings (pgvector).
- **Summarization**: Extractive (default) with optional abstractive summarization.
- **Ranking**: Reciprocal Rank Fusion (RRF) baseline for hybrid ranking.
- **Multi-tenancy**: **Data model and database are multi-tenant** (`tenant_id` on each entity) for forward compatibility; **MVP uses a single hardcoded tenant (e.g., `tenant_id=1`)** to minimize complexity.
- **API surface**: Matches the original task exactly:  
  - `POST /clients/{id}/documents`  
  - `POST /clients/{id}/notes`  
  - `GET /search?q=...&type=document|note`
- **Implementation efficiency**: Realistic for ~12 hours of development.
- **Scalability ready**: Design remains open to future scaling; **not prioritized in MVP** to save time.

---

## 2. Tech Stack Decisions

### API Layer
- **Framework**: FastAPI (async) for rapid development, performance, and automatic OpenAPI/Swagger.
- **Data models & validation**: **Pydantic** schemas for request/response contracts (spec-driven).
- **DB access**: SQLAlchemy 2.x (or lightweight query layer) with `psycopg2`/`asyncpg`.

### Database & Indexing
- **PostgreSQL 15+** with **pgvector** extension.
- **Roles**:
  - Relational store: `tenants`, `clients`, `documents`, `meeting_notes`.
  - Full-text search: `tsvector` + GIN indexes on content fields.
  - Vector similarity: `vector(dim)` columns + ivfflat/HNSW indexes for embeddings.

### Embeddings
- **Default**: Local open-source via `sentence-transformers/all-MiniLM-L6-v2` (384-dim). Zero per-use cost, data remains in-house.
- **Optional**: Abstraction allows switching to external APIs (e.g., Gemini/OpenAI) if higher quality is needed.
- **Abstraction**: `Embedder` interface with providers (`local`, `openai`, `gemini`).

### Summarization (3-Phase Strategy)
- **Phase 1 (MVP)**: Extractive summarization using **Sumy (LexRank)** for safety, speed, and deterministic output.
- **Phase 2 (AI-Enhanced)**: Abstractive summarization using **Gemini API** with custom prompts for custom summarization optimization.
- **Phase 3 (Self-Hosted AI)**: Abstractive summarization using **HuggingFace BART** via transformers pipeline for full control and privacy.
- **Configuration**: Provider switch via `SUMMARIZER=extractive|gemini|bart` environment variable.
- **Strategy**: Precompute and store `summary` at ingestion to keep search latency low.

### Ranking
- **Baseline**: **Reciprocal Rank Fusion (RRF, k=60)** to merge FTS and vector result lists without score normalization.
- **Extensible**: Score fusion or ML re-ranker (cross-encoder) can be introduced later.

### Multi-Tenancy
- **Schema-level**: `tenant_id` on `clients`, `documents`, `meeting_notes`.
- **MVP simplification**: All API paths implicitly operate with `tenant_id=1` (hardcoded in DB queries/config), so no auth logic is required.
- **Future**: Introduce auth middleware to derive `tenant_id` from JWT/session and enable Postgres Row-Level Security (RLS).

### Deployment
- **Docker Compose** with two core services:
  - `api`: FastAPI app with embeddings & summarization packaged.
  - `db`: Postgres with pgvector extension, persistent volume.
- Simple for local dev; portable to K8s/cloud later.

---

## 3. High-Level Architecture

### 3.1 Components
- **Client Applications**: Upload documents/notes, perform searches.
- **API Service (FastAPI)**: Ingestion and search endpoints, orchestrates FTS + vector search, ranking, and summarization.
- **Database (PostgreSQL + pgvector)**: Relational storage, FTS indices, embedding vectors.
- **Embedding Generator**: Local model or external provider via `Embedder` abstraction.
- **Summarizer**: Extractive (default) or abstractive module.

### 3.2 Ingestion Flow
1. `POST /clients/{id}/documents|notes` with JSON payload.
2. Validate request (Pydantic). Check `client_id` exists (and belongs to `tenant_id=1` in MVP).
3. Insert record (content + metadata). `content_tsv` generated via stored expression.
4. Generate and store `content_embedding` (local model by default).
5. Generate and store `summary` (extractive by default).
6. Return `201` with the created object (including `summary` and full `content`).

### 3.3 Search Flow
1. `GET /search?q=...&type=document|note`.
2. Parse query → build `tsquery` and generate `query_embedding`.
3. Execute **FTS** query (GIN) and **vector** query (pgvector) against `tenant_id=1` and selected `type`.
4. Merge ranked lists via **RRF (k=60)**.
5. Fetch top-K full records; return objects with `content`, `summary`, `metadata`, and optional `score`.

---

## 4. Database Schema (DDL)

```sql
CREATE EXTENSION IF NOT EXISTS vector;

-- Tenants (multi-tenant ready; MVP uses tenant_id=1)
CREATE TABLE tenants (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

-- Clients
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    tenant_id INT NOT NULL REFERENCES tenants(id),
    first_name TEXT,
    last_name TEXT,
    email TEXT UNIQUE
);

-- Documents
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    tenant_id INT NOT NULL REFERENCES tenants(id),
    client_id INT NOT NULL REFERENCES clients(id),
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    summary TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    content_embedding vector(384),
    content_tsv tsvector GENERATED ALWAYS AS (to_tsvector('english', content)) STORED
);

-- Meeting Notes
CREATE TABLE meeting_notes (
    id SERIAL PRIMARY KEY,
    tenant_id INT NOT NULL REFERENCES tenants(id),
    client_id INT NOT NULL REFERENCES clients(id),
    content TEXT NOT NULL,
    summary TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    content_embedding vector(384),
    content_tsv tsvector GENERATED ALWAYS AS (to_tsvector('english', content)) STORED
);

-- Indexes (FTS + vector)
CREATE INDEX idx_documents_tsv ON documents USING GIN(content_tsv);
CREATE INDEX idx_notes_tsv     ON meeting_notes USING GIN(content_tsv);

-- Vector index: choose ivfflat (requires ANALYZE and suitable lists) or HNSW if available
-- Use L2 or cosine ops to match embedding normalization
CREATE INDEX idx_documents_embedding ON documents USING ivfflat (content_embedding vector_l2_ops);
CREATE INDEX idx_notes_embedding     ON meeting_notes USING ivfflat (content_embedding vector_l2_ops);
```

> Note: For `ivfflat`, ensure `SET enable_seqscan = off;` and perform `ANALYZE` after bulk inserts. If the Postgres/pgvector build supports `HNSW`, substitute accordingly.

---

## 5. API Specification (exact to original)

### POST `/clients/{id}/documents`
**Description**: Upload a document (title + content) for a client `{id}` (MVP assumes tenant_id=1).  
**Request (application/json)**:
```json
{
  "title": "Retirement Plan 2025",
  "content": "Full text of the document..."
}
```
**Responses**:
- **201 Created**:
```json
{
  "id": 123,
  "client_id": 45,
  "title": "Retirement Plan 2025",
  "content": "Full text of the document...",
  "summary": "Short extractive/abstractive summary...",
  "created_at": "2025-09-15T20:30:00Z"
}
```
- **400 Bad Request** (validation errors), **404 Not Found** (client not found), **500** on unexpected errors.

---

### POST `/clients/{id}/notes`
**Description**: Upload a meeting note (content) for a client `{id}` (MVP assumes tenant_id=1).  
**Request (application/json)**:
```json
{
  "content": "Discussion about portfolio allocation..."
}
```
**Responses**:
- **201 Created**:
```json
{
  "id": 789,
  "client_id": 45,
  "content": "Discussion about portfolio allocation...",
  "summary": "Short extractive/abstractive summary...",
  "created_at": "2025-09-15T21:00:00Z"
}
```
- **400**, **404**, **500** as applicable.

---

### GET `/search?q=...&type=document|note`
**Description**: Hybrid search across documents and/or notes for the MVP tenant (`tenant_id=1`).  
**Query params**:
- `q` (string, required): query text.
- `type` (string, optional): `document` or `note`. If omitted, search both.

**Response 200 (example)**:
```json
{
  "query": "retirement plan",
  "type": "document",
  "results": [
    {
      "id": 123,
      "type": "document",
      "client_id": 45,
      "title": "Retirement Plan 2025",
      "content": "Full text...",
      "summary": "Short summary...",
      "created_at": "2025-08-01T10:00:00Z",
      "score": 0.95
    },
    {
      "id": 789,
      "type": "note",
      "client_id": 45,
      "content": "Discussion about allocation...",
      "summary": "Short summary...",
      "created_at": "2025-09-01T15:30:00Z",
      "score": 0.89
    }
  ]
}
```

---

## 6. Component Design

### 6.1 API Service (FastAPI + Pydantic)
- **Routers**: `/clients/{id}/documents`, `/clients/{id}/notes`, `/search`.
- **Schemas (Pydantic)**: `DocumentCreate`, `NoteCreate`, `SearchResponse`, `SearchResult`.
- **DB session**: dependency-injected session per request.
- **Embedding/Summarization**: initialized at startup; provider switch via config env (`EMBEDDINGS_PROVIDER=local|openai|gemini`, `SUMMARIZER=extractive|abstractive`).
- **MVP Tenant**: constant `TENANT_ID=1` injected into all queries.

### 6.2 Embedding Generator
- **Local (default)**: `SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')`; `encode(text, normalize_embeddings=True)`.
- **External (optional)**: provider class for OpenAI/Gemini embeddings.

### 6.3 Summarizer
- **Extractive**: Sumy (LexRank) with configurable sentence count (e.g., 3–5).
- **Abstractive (Gemini)**: Google Gemini API with custom summarization prompts for enhanced quality.
- **Abstractive (BART)**: HuggingFace BART pipeline for self-hosted abstractive summarization with full privacy control.

### 6.4 Hybrid Ranker (RRF)
- Run FTS (ts_rank) and vector similarity queries (distance ascending).
- Merge top-N from each (e.g., 50/50) via RRF(k=60); return top-K (e.g., 10–20).

### 6.5 Error Handling & Limits
- **Validation**: Empty `q`, overly large `content` (consider max size), unsupported `type` → 400.
- **Time limits**: Reasonable DB timeouts; summarize/embedding protected by try/except with clear 500 on failure.
- **Security**: No auth in MVP; **all queries scoped to `tenant_id=1`**.

---

## 7. Docker Compose

`docker-compose.yml` (high level):
```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/wealthtech_db
      - TENANT_ID=1
      - EMBEDDINGS_PROVIDER=local
      - SUMMARIZER=extractive
    depends_on:
      - db
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
      - hf_cache:/root/.cache/huggingface

  db:
    image: pgvector/pgvector:pg16
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=wealthtech_db
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d wealthtech_db"]
      interval: 5s
      timeout: 5s
      retries: 10

volumes:
  pg_data:
  hf_cache:
```

`Dockerfile` (outline):
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

`requirements.txt` (core):
```
fastapi
uvicorn[standard]
pydantic
sqlalchemy
psycopg2-binary
pgvector
sentence-transformers
sumy
httpx
```

---

## 8. Testing Strategy

### Unit Tests
- **Ranker**: RRF correctness with known lists.
- **Embedder/Summarizer**: Stub providers return deterministic outputs.
- **Validation**: Pydantic schema tests for required fields and errors.
- **Tenant scoping**: Query builders inject `tenant_id=1`.

### Integration Tests
- **Ingestion → Search**: Insert sample data; verify hybrid search returns expected results.
- **FTS vs vector**: Queries that only one method catches; ensure RRF merges properly.
- **Performance sanity**: Single search <~500ms on small dataset (local).

### Manual QA
- Swagger UI sanity (FastAPI auto-docs).
- Postman for end-to-end checks.
- Human relevance evaluation on curated dataset.

---

## 9. Trade-offs & Assumptions

- **Local AI**: Lower cost, slightly lower accuracy than premium APIs; switch available.
- **Postgres-only**: Simpler ops; for very large scale consider external search/vector services.
- **Synchronous ingestion**: Ensures immediate availability; increases write latency slightly.
- **Full content in results**: Heavier payloads; improves reviewability as per requirement.
- **Multi-tenancy**: Implemented at schema level; **MVP uses single hardcoded tenant** to save time.

---

## 10. Scalability & Extension (Not prioritized in MVP)

- **Async ingestion** (background jobs) for embeddings/summaries.
- **Caching** of frequent queries and embeddings.
- **DB scaling**: read replicas, partitioning by tenant/date, connection pooling.
- **Inference separation**: move embeddings/summarization to a worker pool or standalone service.
- **Reranking**: Cross-encoder re-ranker for top-N.
- **RAG/QA**: Add `/ask` with retrieval-augmented generation on top-k results.
- **Auth/RLS**: Introduce JWT auth; enforce Postgres RLS for true tenant isolation.

---

## 11. Development Plan & Time Estimates (~16 hours)

| Task | Estimate |
|------|----------|
| Project scaffolding (FastAPI, structure, Pydantic models) | 1.0h |
| DB setup (Docker, pgvector, schema & indexes) | 1.5h |
| Embedder (local MiniLM) abstraction & wiring | 1.0h |
| Summarizer Phase 1 (Sumy LexRank extractive) | 1.5h |
| Ingestion endpoints (docs/notes) + persistence | 1.5h |
| Summarizer Phase 2 (Gemini API abstractive with custom summarization prompts) | 2.0h |
| Summarizer Phase 3 (HuggingFace BART self-hosted abstractive) | 2.0h |
| Search pipeline (FTS + vector + RRF + response shaping) | 2.0h |
| API docs (OpenAPI via FastAPI) + README usage examples | 1.0h |
| Tests (unit + integration) | 1.5h |
| Docker Compose & local runbook | 1.0h |
| Buffer/Polish | 1.0h |

**Total**: ~16 hours

---

## 12. Conclusion
This design delivers an MVP-ready **Smart Search API** that adheres to the original task’s API routes while being **multi-tenant ready** at the data layer. It uses **FastAPI + Pydantic**, **Postgres FTS + pgvector**, a **local embedding model**, and **extractive summaries** by default. The design is intentionally lean for fast delivery, with clear pathways to scale capabilities and performance later.
