CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS app;
CREATE SCHEMA IF NOT EXISTS rag;

CREATE TABLE IF NOT EXISTS app.documents (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    title varchar(200) NOT NULL CHECK (char_length(trim(title)) BETWEEN 1 AND 200),
    source varchar(500) NOT NULL CHECK (char_length(trim(source)) BETWEEN 1 AND 500),
    status varchar(24) NOT NULL DEFAULT 'queued'
        CHECK (status IN ('queued', 'running', 'completed', 'failed')),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS app.document_versions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id uuid NOT NULL REFERENCES app.documents(id) ON DELETE CASCADE,
    version integer NOT NULL CHECK (version > 0),
    filename varchar(255) NOT NULL,
    media_type varchar(100) NOT NULL,
    byte_size integer NOT NULL CHECK (byte_size > 0),
    content_sha256 char(64) NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (document_id, version),
    UNIQUE (content_sha256)
);

CREATE TABLE IF NOT EXISTS app.ingestion_jobs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id uuid NOT NULL REFERENCES app.documents(id) ON DELETE CASCADE,
    document_version_id uuid NOT NULL REFERENCES app.document_versions(id) ON DELETE CASCADE,
    idempotency_key varchar(128) NOT NULL UNIQUE,
    status varchar(24) NOT NULL DEFAULT 'queued'
        CHECK (status IN ('queued', 'running', 'completed', 'failed')),
    chunk_count integer NOT NULL DEFAULT 0 CHECK (chunk_count >= 0),
    embedding_version_id uuid,
    error_code varchar(80),
    error_message varchar(500),
    started_at timestamptz,
    completed_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS rag.embedding_versions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    provider varchar(80) NOT NULL,
    model varchar(160) NOT NULL,
    dimension integer NOT NULL CHECK (dimension > 0),
    preprocessing_version varchar(80) NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (provider, model, dimension, preprocessing_version)
);

CREATE TABLE IF NOT EXISTS rag.ingestion_receipts (
    job_id uuid PRIMARY KEY,
    document_id uuid NOT NULL,
    document_version_id uuid NOT NULL,
    status varchar(24) NOT NULL
        CHECK (status IN ('running', 'completed', 'failed')),
    chunk_count integer NOT NULL DEFAULT 0 CHECK (chunk_count >= 0),
    embedding_version_id uuid REFERENCES rag.embedding_versions(id),
    error_code varchar(80),
    error_message varchar(500),
    started_at timestamptz NOT NULL DEFAULT now(),
    completed_at timestamptz
);

CREATE TABLE IF NOT EXISTS rag.chunks (
    id uuid PRIMARY KEY,
    document_id uuid NOT NULL,
    document_version_id uuid NOT NULL,
    chunk_index integer NOT NULL CHECK (chunk_index >= 0),
    chunking_version varchar(80) NOT NULL,
    content text NOT NULL CHECK (char_length(content) > 0),
    start_offset integer NOT NULL CHECK (start_offset >= 0),
    end_offset integer NOT NULL CHECK (end_offset > start_offset),
    locator jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (document_version_id, chunk_index)
);

CREATE TABLE IF NOT EXISTS rag.chunk_embeddings (
    chunk_id uuid NOT NULL REFERENCES rag.chunks(id) ON DELETE CASCADE,
    embedding_version_id uuid NOT NULL REFERENCES rag.embedding_versions(id),
    embedding vector(128) NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (chunk_id, embedding_version_id)
);

CREATE TABLE IF NOT EXISTS rag.citations (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    query_hash char(64) NOT NULL,
    chunk_id uuid NOT NULL REFERENCES rag.chunks(id) ON DELETE CASCADE,
    score double precision NOT NULL CHECK (score >= -1 AND score <= 1),
    snippet text NOT NULL,
    locator jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (query_hash, chunk_id)
);

CREATE INDEX IF NOT EXISTS chunks_document_idx ON rag.chunks(document_id, document_version_id);
CREATE INDEX IF NOT EXISTS citations_chunk_idx ON rag.citations(chunk_id);

COMMENT ON SCHEMA app IS 'Owned by the NestJS public API.';
COMMENT ON SCHEMA rag IS 'Owned by the internal Python RAG service.';
COMMENT ON COLUMN rag.chunk_embeddings.embedding IS 'Sprint 1 exact cosine reference search; no ANN index without benchmark evidence.';
