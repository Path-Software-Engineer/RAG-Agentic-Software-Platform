export type DocumentStatus = 'queued' | 'running' | 'completed' | 'failed';

export interface DocumentResource {
  documentId: string;
  documentVersionId: string;
  jobId: string;
  title: string;
  source: string;
  filename: string;
  status: DocumentStatus;
  chunkCount: number;
  embeddingVersionId: string | null;
  createdAt: string;
  correlationId: string;
  deduplicated: boolean;
}

export interface SearchResultResource {
  rank: number;
  score: number;
  documentId: string;
  documentVersionId: string;
  chunkId: string;
  citationId: string;
  title: string;
  source: string;
  snippet: string;
  locator: Record<string, unknown>;
}

export interface SearchResponseResource {
  query: string;
  topK: number;
  embeddingVersionId: string;
  scoreSemantics: string;
  elapsedMs: number;
  correlationId: string;
  results: SearchResultResource[];
}

export interface CitationResource {
  citationId: string;
  documentId: string;
  documentVersionId: string;
  chunkId: string;
  title: string;
  source: string;
  score: number;
  snippet: string;
  content: string;
  locator: Record<string, unknown>;
  correlationId: string;
}

export interface ApiErrorResource {
  code: string;
  message: string;
  details: Record<string, unknown>;
  correlationId: string;
}

export interface EvaluationStrategyResource {
  strategyId: string;
  label: string;
  description: string;
  chunkSize: number;
  overlap: number;
  boundary: string;
}

export interface EvaluationTestCaseResource {
  testCaseId: string;
  query: string;
  relevantDocumentIds: string[];
  rationale: string;
  createdAt: string;
}

export interface EvaluationHitResource {
  resultId: string;
  rank: number;
  score: number;
  documentId: string;
  documentVersionId: string;
  chunkId: string;
  title: string;
  source: string;
  snippet: string;
  locator: Record<string, unknown>;
  relevant: boolean;
  relevanceSource: 'expected-set' | 'manual';
  relevanceNotes: string | null;
}

export interface EvaluationQueryResource {
  testCaseId: string;
  query: string;
  expectedDocumentIds: string[];
  precisionAtK: number;
  recallAtK: number;
  hit: boolean;
  reciprocalRank: number;
  results: EvaluationHitResource[];
}

export interface StrategyMetricsResource {
  strategyId: string;
  strategyLabel: string;
  queryCount: number;
  chunkCount: number;
  precisionAtK: number;
  recallAtK: number;
  hitRate: number;
  meanReciprocalRank: number;
  errorCount: number;
}

export interface EvaluationStrategyResultResource {
  metrics: StrategyMetricsResource;
  queries: EvaluationQueryResource[];
}

export interface EvaluationRunResource {
  runId: string;
  status: 'completed';
  topK: number;
  strategyIds: string[];
  testCaseIds: string[];
  documentVersionIds: string[];
  embeddingVersion: string;
  scoreSemantics: string;
  metricSemantics: string;
  strategies: EvaluationStrategyResultResource[];
  createdAt: string;
  completedAt: string;
  elapsedMs: number;
  correlationId: string;
}

export interface EvaluationRunSummaryResource {
  runId: string;
  topK: number;
  strategyCount: number;
  queryCount: number;
  bestStrategyId: string;
  bestRecallAtK: number;
  createdAt: string;
}

export type AgentRunStatus =
  | 'queued'
  | 'running'
  | 'waiting'
  | 'completed'
  | 'failed'
  | 'cancelled'
  | 'blocked';

export interface AgentRunResource {
  runId: string;
  threadId: string;
  workflowId: string;
  status: AgentRunStatus;
  outcome: string | null;
  goal: string;
  answer: string | null;
  allowedToolNames: string[];
  documentVersionIds: string[];
  budget: {
    maxSteps: number;
    maxToolCalls: number;
    overallTimeoutMs: number;
    perToolTimeoutMs: number;
  };
  usage: { steps: number; toolCalls: number; elapsedMs: number };
  citations: Array<{
    citationId: string;
    documentId: string;
    documentVersionId: string;
    chunkId: string;
    rank: number;
    score: number;
    snippet: string;
  }>;
  correlationId: string;
  createdAt: string;
  startedAt: string | null;
  completedAt: string | null;
  errorCode: string | null;
}

export interface AgentRunSummaryResource {
  runId: string;
  workflowId: string;
  status: AgentRunStatus;
  outcome: string | null;
  goal: string;
  citationCount: number;
  createdAt: string;
  completedAt: string | null;
}

export interface AgentTraceEventResource {
  eventId: string;
  runId: string;
  sequenceNumber: number;
  eventType: string;
  nodeId: string | null;
  payload: Record<string, unknown>;
  timestamp: string;
}

export interface AgentTraceResource {
  run: AgentRunResource;
  nodes: Array<{ nodeId: string; label: string; kind: string }>;
  edges: Array<{ source: string; target: string; condition: string }>;
  steps: Array<{
    stepId: string;
    nodeId: string;
    sequenceNumber: number;
    status: string;
    startedAt: string;
    completedAt: string | null;
    durationMs: number | null;
    errorCode: string | null;
  }>;
  toolCalls: Array<{
    toolCallId: string;
    stepId: string;
    toolName: string;
    status: string;
    sanitizedArguments: Record<string, unknown>;
    sanitizedResult: Record<string, unknown> | null;
    startedAt: string;
    completedAt: string | null;
    durationMs: number | null;
    errorCode: string | null;
  }>;
  events: AgentTraceEventResource[];
  privateReasoningExposed: false;
}

export interface ToolDefinitionResource {
  name: string;
  description: string;
  permission: string;
  inputSchema: Record<string, unknown>;
  timeoutMs: number;
  maxResultBytes: number;
  readOnly: true;
}

export interface SecurityEvaluationResource {
  evaluationId: string;
  policyVersion: string;
  scenarioCount: number;
  passedCount: number;
  blockedCount: number;
  failedCount: number;
  passed: boolean;
  scenarios: Array<{
    scenario_id: string;
    category: string;
    expected: string;
    observed: string;
    passed: boolean;
    policy_code: string | null;
  }>;
  createdAt: string;
}
