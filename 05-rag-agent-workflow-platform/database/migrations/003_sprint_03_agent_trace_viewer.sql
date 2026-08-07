CREATE SCHEMA IF NOT EXISTS agent;

CREATE TABLE IF NOT EXISTS agent.agent_runs (
    id uuid PRIMARY KEY,
    thread_id uuid NOT NULL,
    workflow_id varchar(80) NOT NULL CHECK (workflow_id = 'bounded-research-v1'),
    status varchar(20) NOT NULL CHECK (
        status IN ('queued', 'running', 'waiting', 'completed', 'failed', 'cancelled', 'blocked')
    ),
    outcome varchar(40) CHECK (
        outcome IS NULL OR outcome IN (
            'answered', 'insufficient_evidence', 'policy_blocked',
            'budget_exhausted', 'cancelled', 'failed'
        )
    ),
    goal varchar(500) NOT NULL CHECK (char_length(trim(goal)) >= 3),
    idempotency_key varchar(120) NOT NULL UNIQUE,
    correlation_id uuid NOT NULL,
    snapshot jsonb NOT NULL,
    created_at timestamptz NOT NULL,
    started_at timestamptz,
    completed_at timestamptz
);

CREATE TABLE IF NOT EXISTS agent.agent_steps (
    id uuid PRIMARY KEY,
    run_id uuid NOT NULL REFERENCES agent.agent_runs(id) ON DELETE CASCADE,
    node_id varchar(80) NOT NULL,
    sequence_number integer NOT NULL CHECK (sequence_number > 0),
    status varchar(20) NOT NULL CHECK (
        status IN ('running', 'completed', 'failed', 'blocked', 'cancelled')
    ),
    started_at timestamptz NOT NULL,
    completed_at timestamptz,
    duration_ms double precision CHECK (duration_ms IS NULL OR duration_ms >= 0),
    error_code varchar(80),
    UNIQUE (run_id, sequence_number)
);

CREATE TABLE IF NOT EXISTS agent.tool_calls (
    id uuid PRIMARY KEY,
    run_id uuid NOT NULL REFERENCES agent.agent_runs(id) ON DELETE CASCADE,
    step_id uuid NOT NULL REFERENCES agent.agent_steps(id) ON DELETE CASCADE,
    tool_name varchar(80) NOT NULL CHECK (
        tool_name IN ('semantic_search', 'document_lookup', 'evaluation_lookup')
    ),
    status varchar(20) NOT NULL CHECK (status IN ('running', 'completed', 'failed', 'blocked')),
    sanitized_arguments jsonb NOT NULL,
    sanitized_result jsonb,
    started_at timestamptz NOT NULL,
    completed_at timestamptz,
    duration_ms double precision CHECK (duration_ms IS NULL OR duration_ms >= 0),
    error_code varchar(80)
);

CREATE TABLE IF NOT EXISTS agent.trace_events (
    id uuid PRIMARY KEY,
    run_id uuid NOT NULL REFERENCES agent.agent_runs(id) ON DELETE CASCADE,
    sequence_number integer NOT NULL CHECK (sequence_number > 0),
    event_type varchar(40) NOT NULL CHECK (
        event_type IN (
            'run_started', 'step_started', 'step_completed', 'step_failed',
            'tool_called', 'tool_completed', 'tool_failed', 'policy_blocked',
            'run_completed', 'run_failed', 'run_cancelled'
        )
    ),
    node_id varchar(80),
    payload jsonb NOT NULL,
    created_at timestamptz NOT NULL,
    UNIQUE (run_id, sequence_number)
);

CREATE TABLE IF NOT EXISTS agent.agent_checkpoints (
    run_id uuid PRIMARY KEY REFERENCES agent.agent_runs(id) ON DELETE CASCADE,
    sequence_number integer NOT NULL CHECK (sequence_number > 0),
    state jsonb NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS agent.security_evaluations (
    id uuid PRIMARY KEY,
    policy_version varchar(80) NOT NULL,
    snapshot jsonb NOT NULL,
    passed boolean NOT NULL,
    created_at timestamptz NOT NULL
);

CREATE INDEX IF NOT EXISTS agent_runs_created_idx
    ON agent.agent_runs(created_at DESC);
CREATE INDEX IF NOT EXISTS trace_events_run_sequence_idx
    ON agent.trace_events(run_id, sequence_number);
CREATE INDEX IF NOT EXISTS tool_calls_run_started_idx
    ON agent.tool_calls(run_id, started_at);

COMMENT ON SCHEMA agent IS
    'Sprint 3 governed workflow state; PostgreSQL is durable and Redis Streams is transient.';
COMMENT ON TABLE agent.trace_events IS
    'Sanitized operational events only; private reasoning and secret-bearing payloads are forbidden.';
