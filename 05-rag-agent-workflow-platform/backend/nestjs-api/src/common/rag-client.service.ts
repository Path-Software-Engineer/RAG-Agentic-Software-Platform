import { Injectable } from '@nestjs/common';
import { ApplicationError } from './error.filter';

export interface InternalIngestionRequest {
  job_id: string;
  document_id: string;
  document_version_id: string;
  filename: string;
  media_type: 'text/plain' | 'text/markdown';
  content: string;
  content_sha256: string;
  correlation_id: string;
}

export interface InternalIngestionResponse {
  job_id: string;
  status: 'running' | 'completed' | 'failed';
  chunk_count: number;
  embedding_version_id: string | null;
  elapsed_ms: number;
  correlation_id: string;
}

export interface InternalSearchResponse {
  query: string;
  top_k: number;
  embedding_version_id: string;
  score_semantics: string;
  elapsed_ms: number;
  correlation_id: string;
  results: Array<{
    rank: number;
    score: number;
    document_id: string;
    document_version_id: string;
    chunk_id: string;
    citation_id: string;
    snippet: string;
    locator: Record<string, unknown>;
  }>;
}

export interface InternalCitationResponse {
  citation_id: string;
  document_id: string;
  document_version_id: string;
  chunk_id: string;
  score: number;
  snippet: string;
  content: string;
  locator: Record<string, unknown>;
}

export interface InternalEvaluationStrategy {
  strategy_id: string;
  label: string;
  description: string;
  chunk_size: number;
  overlap: number;
  boundary: string;
}

export interface InternalEvaluationTestCase {
  test_case_id: string;
  query: string;
  relevant_document_ids: string[];
  rationale: string;
  created_at: string;
}

export interface InternalEvaluationHit {
  result_id: string;
  rank: number;
  score: number;
  document_id: string;
  document_version_id: string;
  chunk_id: string;
  snippet: string;
  locator: Record<string, unknown>;
  relevant: boolean;
  relevance_source: 'expected-set' | 'manual';
  relevance_notes: string | null;
}

export interface InternalEvaluationRun {
  run_id: string;
  status: 'completed';
  top_k: number;
  strategy_ids: string[];
  test_case_ids: string[];
  document_version_ids: string[];
  embedding_version: string;
  score_semantics: string;
  metric_semantics: string;
  strategies: Array<{
    metrics: {
      strategy_id: string;
      strategy_label: string;
      query_count: number;
      chunk_count: number;
      precision_at_k: number;
      recall_at_k: number;
      hit_rate: number;
      mean_reciprocal_rank: number;
      error_count: number;
    };
    queries: Array<{
      test_case_id: string;
      query: string;
      expected_document_ids: string[];
      precision_at_k: number;
      recall_at_k: number;
      hit: boolean;
      reciprocal_rank: number;
      results: InternalEvaluationHit[];
    }>;
  }>;
  created_at: string;
  completed_at: string;
  elapsed_ms: number;
  correlation_id: string;
}

export interface InternalEvaluationRunSummary {
  run_id: string;
  top_k: number;
  strategy_count: number;
  query_count: number;
  best_strategy_id: string;
  best_recall_at_k: number;
  created_at: string;
}

export interface InternalAgentRun {
  run_id: string;
  thread_id: string;
  workflow_id: string;
  status: 'queued' | 'running' | 'waiting' | 'completed' | 'failed' | 'cancelled' | 'blocked';
  outcome: 'answered' | 'insufficient_evidence' | 'policy_blocked' | 'budget_exhausted' | 'cancelled' | 'failed' | null;
  goal: string;
  answer: string | null;
  allowed_tool_names: string[];
  document_version_ids: string[];
  budget: {
    max_steps: number;
    max_tool_calls: number;
    overall_timeout_ms: number;
    per_tool_timeout_ms: number;
  };
  usage: { steps: number; tool_calls: number; elapsed_ms: number };
  citations: Array<{
    citation_id: string;
    document_id: string;
    document_version_id: string;
    chunk_id: string;
    rank: number;
    score: number;
    snippet: string;
  }>;
  idempotency_key: string;
  correlation_id: string;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
  error_code: string | null;
}

export interface InternalAgentRunSummary {
  run_id: string;
  workflow_id: string;
  status: InternalAgentRun['status'];
  outcome: InternalAgentRun['outcome'];
  goal: string;
  citation_count: number;
  created_at: string;
  completed_at: string | null;
}

export interface InternalAgentTraceEvent {
  event_id: string;
  run_id: string;
  sequence_number: number;
  event_type: string;
  node_id: string | null;
  payload: Record<string, unknown>;
  timestamp: string;
}

export interface InternalAgentTrace {
  run: InternalAgentRun;
  nodes: Array<{ node_id: string; label: string; kind: string }>;
  edges: Array<Record<string, unknown>>;
  steps: Array<{
    step_id: string;
    node_id: string;
    sequence_number: number;
    status: string;
    started_at: string;
    completed_at: string | null;
    duration_ms: number | null;
    error_code: string | null;
  }>;
  tool_calls: Array<{
    tool_call_id: string;
    step_id: string;
    tool_name: string;
    status: string;
    sanitized_arguments: Record<string, unknown>;
    sanitized_result: Record<string, unknown> | null;
    started_at: string;
    completed_at: string | null;
    duration_ms: number | null;
    error_code: string | null;
  }>;
  events: InternalAgentTraceEvent[];
  private_reasoning_exposed: false;
}

export interface InternalToolDefinition {
  name: string;
  description: string;
  permission: string;
  input_schema: Record<string, unknown>;
  timeout_ms: number;
  max_result_bytes: number;
  read_only: true;
}

export interface InternalSecurityEvaluation {
  evaluation_id: string;
  policy_version: string;
  scenario_count: number;
  passed_count: number;
  blocked_count: number;
  failed_count: number;
  passed: boolean;
  scenarios: Array<Record<string, unknown>>;
  created_at: string;
}

@Injectable()
export class RagClient {
  private readonly baseUrl = process.env.RAG_SERVICE_URL ?? 'http://localhost:58100';

  ingest(payload: InternalIngestionRequest): Promise<InternalIngestionResponse> {
    return this.request('/internal/v1/ingestions', 'POST', payload, payload.correlation_id);
  }

  search(
    payload: {
      query: string;
      top_k: number;
      document_ids: string[];
      document_version_ids: string[];
      correlation_id: string;
    },
  ): Promise<InternalSearchResponse> {
    return this.request('/internal/v1/retrieval/search', 'POST', payload, payload.correlation_id);
  }

  citation(citationId: string, correlationId: string): Promise<InternalCitationResponse> {
    return this.request(
      `/internal/v1/citations/${encodeURIComponent(citationId)}`,
      'GET',
      undefined,
      correlationId,
    );
  }

  evaluationStrategies(correlationId: string): Promise<InternalEvaluationStrategy[]> {
    return this.request('/internal/v1/evaluations/strategies', 'GET', undefined, correlationId);
  }

  evaluationTestCases(correlationId: string): Promise<InternalEvaluationTestCase[]> {
    return this.request('/internal/v1/evaluations/test-cases', 'GET', undefined, correlationId);
  }

  createEvaluationTestCase(
    payload: { query: string; relevant_document_ids: string[]; rationale: string },
    correlationId: string,
  ): Promise<InternalEvaluationTestCase> {
    return this.request('/internal/v1/evaluations/test-cases', 'POST', payload, correlationId);
  }

  evaluationRuns(correlationId: string): Promise<InternalEvaluationRunSummary[]> {
    return this.request('/internal/v1/evaluations/runs', 'GET', undefined, correlationId);
  }

  createEvaluationRun(
    payload: {
      strategy_ids: string[];
      test_case_ids: string[];
      document_version_ids: string[];
      top_k: number;
      correlation_id: string;
    },
  ): Promise<InternalEvaluationRun> {
    return this.request('/internal/v1/evaluations/runs', 'POST', payload, payload.correlation_id);
  }

  evaluationRun(runId: string, correlationId: string): Promise<InternalEvaluationRun> {
    return this.request(
      `/internal/v1/evaluations/runs/${encodeURIComponent(runId)}`,
      'GET',
      undefined,
      correlationId,
    );
  }

  labelEvaluationResult(
    runId: string,
    resultId: string,
    payload: { relevant: boolean; notes?: string; correlation_id: string },
  ): Promise<InternalEvaluationRun> {
    return this.request(
      `/internal/v1/evaluations/runs/${encodeURIComponent(runId)}/results/${encodeURIComponent(resultId)}/relevance`,
      'PATCH',
      payload,
      payload.correlation_id,
    );
  }

  agentTools(correlationId: string): Promise<InternalToolDefinition[]> {
    return this.request('/internal/v1/agents/tools', 'GET', undefined, correlationId);
  }

  createAgentRun(payload: {
    goal: string;
    workflow_id: string;
    document_version_ids: string[];
    allowed_tool_names: string[];
    budget: {
      max_steps: number;
      max_tool_calls: number;
      overall_timeout_ms: number;
      per_tool_timeout_ms: number;
    };
    idempotency_key: string;
    correlation_id: string;
  }): Promise<InternalAgentRun> {
    return this.request('/internal/v1/agents/runs', 'POST', payload, payload.correlation_id);
  }

  agentRuns(correlationId: string): Promise<InternalAgentRunSummary[]> {
    return this.request('/internal/v1/agents/runs', 'GET', undefined, correlationId);
  }

  agentRun(runId: string, correlationId: string): Promise<InternalAgentRun> {
    return this.request(
      `/internal/v1/agents/runs/${encodeURIComponent(runId)}`,
      'GET',
      undefined,
      correlationId,
    );
  }

  agentTrace(runId: string, correlationId: string): Promise<InternalAgentTrace> {
    return this.request(
      `/internal/v1/agents/runs/${encodeURIComponent(runId)}/trace`,
      'GET',
      undefined,
      correlationId,
    );
  }

  agentEvents(
    runId: string,
    afterSequence: number,
    correlationId: string,
  ): Promise<InternalAgentTraceEvent[]> {
    return this.request(
      `/internal/v1/agents/runs/${encodeURIComponent(runId)}/events?after_sequence=${afterSequence}`,
      'GET',
      undefined,
      correlationId,
    );
  }

  cancelAgentRun(runId: string, correlationId: string): Promise<InternalAgentRun> {
    return this.request(
      `/internal/v1/agents/runs/${encodeURIComponent(runId)}/cancel`,
      'POST',
      {},
      correlationId,
    );
  }

  securityEvaluation(correlationId: string): Promise<InternalSecurityEvaluation> {
    return this.request('/internal/v1/security/evaluations', 'POST', {}, correlationId);
  }

  private async request<T>(
    path: string,
    method: 'GET' | 'POST' | 'PATCH',
    body: unknown,
    correlationId: string,
  ): Promise<T> {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 12_000);
    try {
      const response = await fetch(`${this.baseUrl}${path}`, {
        method,
        headers: {
          accept: 'application/json',
          'content-type': 'application/json',
          'x-correlation-id': correlationId,
        },
        body: body === undefined ? undefined : JSON.stringify(body),
        signal: controller.signal,
      });
      if (!response.ok) {
        if (response.status === 404) {
          throw new ApplicationError('RAG_RESOURCE_NOT_FOUND', 'The requested evidence was not found.', 404);
        }
        if (response.status === 422) {
          throw new ApplicationError(
            'REQUEST_INVALID',
            'The request is incomplete or inconsistent with the current evidence.',
            422,
          );
        }
        if (response.status === 409) {
          throw new ApplicationError(
            'AGENT_RUN_CONFLICT',
            'The requested run transition is not valid in its current state.',
            409,
          );
        }
        throw new ApplicationError(
          'RAG_SERVICE_REJECTED',
          'The retrieval service rejected the request.',
          502,
        );
      }
      return (await response.json()) as T;
    } catch (error) {
      if (error instanceof ApplicationError) throw error;
      if (error instanceof Error && error.name === 'AbortError') {
        throw new ApplicationError('RAG_SERVICE_TIMEOUT', 'The retrieval service timed out.', 504);
      }
      throw new ApplicationError('RAG_SERVICE_UNAVAILABLE', 'The retrieval service is unavailable.', 503);
    } finally {
      clearTimeout(timeout);
    }
  }
}
