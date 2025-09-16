# Database Initialization - Code Context

## Task Overview
Create database initialization script for WealthTech Smart Search API with PostgreSQL + pgvector extension and multi-tenant schema.

## Requirements
- PostgreSQL 15+ with pgvector extension
- Multi-tenant schema with tenant_id columns
- Full-text search with GIN indexes
- Vector similarity with pgvector indexes (384-dim)
- MVP uses single tenant (tenant_id=1)

## Implementation Path
- Create `init.sql` with schema DDL
- Update `docker-compose.yml` to use initialization script
- Restart database container
- Verify schema creation

## Reference Schema
From WealthTech_Smart_Search_Design.md:
- tenants table
- clients table (with tenant_id FK)
- documents table (with tenant_id, client_id FKs, content_tsv, content_embedding)
- meeting_notes table (with tenant_id, client_id FKs, content_tsv, content_embedding)
- GIN indexes on content_tsv columns
- Vector indexes on content_embedding columns
