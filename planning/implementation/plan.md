# WealthTech Smart Search API - Implementation Prompt Plan

## Checklist
- [x] Step 1: Fix database initialization and schema setup
- [ ] Step 2: Resolve Python import path issues
- [ ] Step 3: Restart and verify API container functionality
- [ ] Step 4: Test all three API endpoints
- [ ] Step 5: Add basic error handling and validation
- [ ] Step 6: Create integration test for end-to-end workflow

## Implementation Prompts

### Step 1 Prompt: Fix database initialization and schema setup

```
Create database initialization script for WealthTech Smart Search API. The database needs PostgreSQL with pgvector extension and tables for multi-tenant architecture (tenant_id=1 for MVP).

Requirements:
- Create init.sql with pgvector extension
- Add tables: tenants, clients, documents, meeting_notes
- Include GIN indexes for full-text search (content_tsv columns)
- Add vector indexes for embeddings (384-dim vectors)
- Update docker-compose.yml to use init script
- Restart database container and verify schema

Reference the design document schema in WealthTech_Smart_Search_Design.md for exact DDL.

Expected outcome: Database running with all tables and indexes, ready for API connection.
```

### Step 2 Prompt: Resolve Python import path issues

```
Fix Python import path issues in the WealthTech Smart Search FastAPI application that are preventing container startup.

Current status: 13 files, 30 symbols implemented but API container crashes on import.

Tasks:
- Use code analysis tools to examine current import structure
- Identify missing __init__.py files or incorrect relative imports
- Fix import paths in FastAPI modules (app/main.py, app/api/, app/services/)
- Ensure all dependencies are properly imported
- Test imports work without errors

Expected outcome: FastAPI application starts successfully without import errors.
```

### Step 3 Prompt: Restart and verify API container functionality

```
Get the WealthTech Smart Search API container running and verify basic functionality after fixing imports.

Tasks:
- Rebuild API container with fixed import paths
- Start API container and verify database connection
- Check FastAPI auto-generated docs at /docs endpoint
- Verify all three endpoints are accessible: POST /clients/{id}/documents, POST /clients/{id}/notes, GET /search
- Test basic health/status endpoint

Expected outcome: API container running, FastAPI docs accessible, endpoints responding (even with validation errors).
```

### Step 4 Prompt: Test all three API endpoints

```
Test and verify all three WealthTech Smart Search API endpoints work with proper request/response handling.

Endpoints to test:
1. POST /clients/{id}/documents - upload document with title and content
2. POST /clients/{id}/notes - upload meeting note with content  
3. GET /search?q=...&type=document|note - search with query parameter

Tasks:
- Create test client record if needed (tenant_id=1)
- Test document upload with sample data
- Test note upload with sample data
- Test search functionality with basic query
- Verify embeddings generation and summarization work
- Check response formats match design specifications

Expected outcome: All endpoints functional with embeddings, summaries, and search results.
```

### Step 5 Prompt: Add basic error handling and validation

```
Implement proper error handling and input validation for the WealthTech Smart Search API.

Tasks:
- Add HTTP error responses for invalid requests (400, 404, 500)
- Implement client existence validation before document/note creation
- Add request size limits and content validation
- Ensure proper error messages with clear descriptions
- Add database connection error handling
- Validate required fields in request bodies

Expected outcome: API handles invalid requests gracefully with proper HTTP status codes and error messages.
```

### Step 6 Prompt: Create integration test for end-to-end workflow

```
Create integration test to verify the complete WealthTech Smart Search workflow from document upload to search results.

Test workflow:
1. Create/verify test client exists
2. Upload a sample document via POST /clients/{id}/documents
3. Upload a sample meeting note via POST /clients/{id}/notes  
4. Perform search query that should return both items
5. Verify search results include summaries and proper RRF ranking
6. Test different search types (document only, note only, both)

Expected outcome: Complete integration test passes, demonstrating hybrid search with summarization works end-to-end.
```

## Usage Instructions

Execute each prompt in sequence. Each prompt is designed to be self-contained and will result in working, demoable functionality. 

**To start:** Copy and paste "Step 1 Prompt" to begin database initialization.

## Current Context
- Design document: WealthTech_Smart_Search_Design.md
- Status document: README.md  
- Implementation: 75% complete (13 files, 30 symbols)
- Architecture: FastAPI + SQLAlchemy + PostgreSQL + pgvector
