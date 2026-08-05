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
