# WealthTech Smart Search API - Implementation Prompt Plan

## Checklist
- [x] Step 1: Fix database initialization and schema setup
- [x] Step 2: Resolve Python import path issues
- [x] Step 3: Restart and verify API container functionality
- [x] Step 4: Test all three API endpoints
- [x] Step 5: Implement Gemini API abstractive summarization (Phase 2)
- [x] Step 6: Implement HuggingFace BART abstractive summarization (Phase 3)
- [x] Step 7: Add basic error handling and validation
- [x] Step 8: Create integration test for end-to-end workflow

## Implementation Prompts

### Step 1 Prompt: Fix database initialization and schema setup ✅ COMPLETED

### Step 2 Prompt: Resolve Python import path issues ✅ COMPLETED

### Step 3 Prompt: Restart and verify API container functionality ✅ COMPLETED

### Step 4 Prompt: Test all three API endpoints ✅ COMPLETED

### Step 5 Prompt: Implement Gemini API abstractive summarization (Phase 2)

```
Implement Gemini API abstractive summarization as Phase 2 of the 3-phase AI summarization strategy for WealthTech Smart Search API.

Requirements:
- Create GeminiSummarizer class following the pattern from /Users/adarwal/code/project_20250801_1553_sierra/src/llm_adapter.py
- Use plug-and-play design with minimal changes to existing summarizer.py
- Add SUMMARIZER=gemini configuration support
- Create financial domain-specific prompts for better summarization quality
- Handle API errors gracefully with fallback to extractive summarization
- Add google-generativeai dependency to requirements.txt
- Update Docker container to support Gemini API key via environment variable

Implementation approach:
1. Study the GeminiAdapter pattern from Sierra project
2. Create minimal GeminiSummarizer class that integrates cleanly
3. Add configuration support for GEMINI_API_KEY environment variable
4. Test with financial documents to verify improved abstractive quality
5. Ensure backward compatibility with existing extractive summarization

Expected outcome: SUMMARIZER=gemini produces high-quality abstractive summaries using Gemini API with summarization domain prompting for meeting summaries, notes and documents.
```

### Step 6 Prompt: Implement HuggingFace BART abstractive summarization (Phase 3)

```
Implement HuggingFace BART abstractive summarization as Phase 3 of the 3-phase AI summarization strategy.

Requirements:
- Create BARTSummarizer class using transformers pipeline
- Add SUMMARIZER=bart configuration support
- Use facebook/bart-large-cnn model for financial document summarization
- Handle model loading and caching efficiently
- Add transformers dependency and update Docker container
- Ensure self-hosted operation with no external API dependencies

Implementation approach:
1. Create BARTSummarizer using HuggingFace transformers pipeline
2. Add model caching and efficient loading
3. Handle long documents with chunking if needed
4. Test summarization quality vs Gemini and extractive methods
5. Update Docker container with model caching volume

Expected outcome: SUMMARIZER=bart produces high-quality abstractive summaries using self-hosted BART model.
```

### Step 7 Prompt: Add comprehensive error handling and validation

```
Implement comprehensive error handling and input validation for the WealthTech Smart Search API.

CRITICAL Requirements (from design document):
1. Client Validation: "Check client_id exists (and belongs to tenant_id=1 in MVP)"
   - Add client existence validation in documents.py and notes.py
   - Return 404 for invalid client_id
   - Ensure client belongs to tenant_id=1

2. HTTP Error Responses:
   - 400 for invalid request data (malformed JSON, missing fields)
   - 404 for non-existent client_id
   - 500 for database connection failures
   - 500 for AI service failures (with graceful fallback)

3. Input Validation:
   - Content length limits (prevent huge documents)
   - Query parameter validation in search endpoint
   - Request size limits

4. Database Error Handling:
   - Wrap database operations in try/catch blocks
   - Handle SQLAlchemy connection errors
   - Add proper error logging

5. AI Service Error Handling:
   - Handle embedding generation failures
   - Handle summarization failures (already has fallback)
   - Ensure graceful degradation

Implementation Tasks:
- Add validate_client_exists() function
- Wrap all API endpoints with proper error handling
- Add input validation decorators/middleware
- Update database.py with connection error handling
- Add proper logging for debugging

Expected outcome: API handles all error scenarios gracefully with proper HTTP status codes and never crashes.
```

### Step 8 Prompt: Create comprehensive integration tests and fix test quality issues

```
Create comprehensive integration tests for the WealthTech Smart Search API and fix existing test quality issues.

Test Quality Issues to Fix:
1. Mock-Heavy Tests: Current tests mock everything and don't test real functionality
   - Replace mock-heavy tests with real integration tests
   - Test actual API endpoints, not just mocked components
   - Test real AI summarization (at least extractive mode)

2. Missing Test Coverage:
   - No tests for API endpoints (documents, notes, search)
   - No tests for error scenarios (404, 500 responses)
   - No tests for search functionality end-to-end
   - No tests for hybrid search ranking

3. AI-Generated Test Smells:
   - Overly verbose docstrings in test files
   - Unnecessary test comments
   - Clean up test structure and naming

Integration Test Workflow:
1. Test client creation and validation
2. Test all 3 summarization modes (extractive, gemini, bart)
3. Upload sample documents and notes with each summarization mode
4. Perform search queries that return results from all modes
5. Verify search results include proper summaries and RRF ranking
6. Test different search types (document only, note only, both)
7. Test error scenarios (invalid client_id, malformed requests)
8. Compare summarization quality across all 3 phases

Expected outcome: 
- Complete integration test suite that tests real functionality
- All error scenarios covered with proper HTTP status code validation
- Clean, maintainable test code without AI-generated verbosity
- Confidence that all 3 AI summarization phases work with hybrid search
```

## Usage Instructions

Execute each prompt in sequence. Each prompt is designed to be self-contained and will result in working, demoable functionality. 

**Current Status:** Steps 1-4 completed. Ready for Step 5 (Gemini integration).

## Current Context
- Design document: WealthTech_Smart_Search_Design.md (updated with 3-phase strategy)
- Status document: README.md  
- Implementation: 85% complete (core functionality working)
- Architecture: FastAPI + SQLAlchemy + PostgreSQL + pgvector
- Next: AI-based summarization phases (Gemini → BART)
