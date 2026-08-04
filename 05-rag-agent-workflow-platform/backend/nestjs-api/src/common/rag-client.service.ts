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

  private async request<T>(
    path: string,
    method: 'GET' | 'POST',
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
