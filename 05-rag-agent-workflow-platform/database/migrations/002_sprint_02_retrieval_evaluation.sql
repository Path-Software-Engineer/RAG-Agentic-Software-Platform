CREATE TABLE IF NOT EXISTS rag.document_sources (
    document_id uuid NOT NULL,
    document_version_id uuid PRIMARY KEY,
    content text NOT NULL CHECK (char_length(content) > 0),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS rag.retrieval_test_cases (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    query varchar(500) NOT NULL CHECK (char_length(trim(query)) >= 2),
    relevant_document_ids uuid[] NOT NULL CHECK (cardinality(relevant_document_ids) > 0),
    rationale varchar(500) NOT NULL CHECK (char_length(trim(rationale)) >= 5),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS rag.evaluation_runs (
    id uuid PRIMARY KEY,
    top_k integer NOT NULL CHECK (top_k BETWEEN 1 AND 10),
    strategy_ids text[] NOT NULL CHECK (cardinality(strategy_ids) > 0),
    test_case_ids uuid[] NOT NULL CHECK (cardinality(test_case_ids) > 0),
    document_version_ids uuid[] NOT NULL CHECK (cardinality(document_version_ids) > 0),
    status varchar(20) NOT NULL CHECK (status IN ('completed')),
    snapshot jsonb NOT NULL,
    correlation_id uuid NOT NULL,
    created_at timestamptz NOT NULL,
    completed_at timestamptz NOT NULL
);

CREATE TABLE IF NOT EXISTS rag.relevance_labels (
    result_id uuid PRIMARY KEY,
    run_id uuid NOT NULL REFERENCES rag.evaluation_runs(id) ON DELETE CASCADE,
    relevant boolean NOT NULL,
    notes varchar(500),
    correlation_id uuid NOT NULL,
    labeled_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS evaluation_runs_created_idx
    ON rag.evaluation_runs(created_at DESC);

COMMENT ON TABLE rag.evaluation_runs IS
    'Sprint 2 versioned metric evidence; manual labels revise the snapshot and are recorded in relevance_labels.';
