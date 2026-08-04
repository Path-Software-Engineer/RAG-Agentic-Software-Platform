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
