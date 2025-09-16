-- ABOUTME: Database initialization script for WealthTech Smart Search API
-- ABOUTME: Creates pgvector extension, multi-tenant schema, and indexes for hybrid search

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

-- Vector indexes for embeddings
CREATE INDEX idx_documents_embedding ON documents USING ivfflat (content_embedding vector_l2_ops);
CREATE INDEX idx_notes_embedding     ON meeting_notes USING ivfflat (content_embedding vector_l2_ops);

-- Insert default tenant for MVP
INSERT INTO tenants (id, name) VALUES (1, 'Default Tenant') ON CONFLICT (id) DO NOTHING;

-- Create a test client for development
INSERT INTO clients (id, tenant_id, first_name, last_name, email) 
VALUES (1, 1, 'Test', 'Client', 'test@example.com') 
ON CONFLICT (email) DO NOTHING;
