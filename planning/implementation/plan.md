# WealthTech Smart Search API - Implementation Prompt Plan

## Checklist
- [x] Step 1: Fix database initialization and schema setup
- [x] Step 2: Resolve Python import path issues
- [x] Step 3: Restart and verify API container functionality
- [x] Step 4: Test all three API endpoints
- [ ] Step 5: Implement Gemini API abstractive summarization (Phase 2)
- [ ] Step 6: Implement HuggingFace BART abstractive summarization (Phase 3)
- [ ] Step 7: Add basic error handling and validation
- [ ] Step 8: Create integration test for end-to-end workflow

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

Expected outcome: SUMMARIZER=gemini produces high-quality abstractive summaries using Gemini API with financial domain optimization.
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

### Step 7 Prompt: Add basic error handling and validation

```
Implement proper error handling and input validation for the WealthTech Smart Search API.

Tasks:
- Add HTTP error responses for invalid requests (400, 404, 500)
- Implement client existence validation before document/note creation
- Add request size limits and content validation
- Ensure proper error messages with clear descriptions
- Add database connection error handling
- Validate required fields in request bodies
- Add graceful fallback for AI summarization failures

Expected outcome: API handles invalid requests gracefully with proper HTTP status codes and error messages.
```

### Step 8 Prompt: Create integration test for end-to-end workflow

```
Create integration test to verify the complete WealthTech Smart Search workflow including all 3 summarization phases.

Test workflow:
1. Create/verify test client exists
2. Test all 3 summarization modes (extractive, gemini, bart)
3. Upload sample documents and notes with each summarization mode
4. Perform search queries that return results from all modes
5. Verify search results include proper summaries and RRF ranking
6. Test different search types (document only, note only, both)
7. Compare summarization quality across all 3 phases

Expected outcome: Complete integration test passes, demonstrating all 3 AI summarization phases work with hybrid search.
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
