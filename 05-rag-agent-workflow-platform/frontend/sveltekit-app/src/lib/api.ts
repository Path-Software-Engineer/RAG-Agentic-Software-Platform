import { env } from '$env/dynamic/public';
import type {
  ApiErrorResource,
  CitationResource,
  DocumentResource,
  EvaluationRunResource,
  EvaluationRunSummaryResource,
  EvaluationStrategyResource,
  EvaluationTestCaseResource,
  SearchResponseResource
} from './types';
export { formatLocator, formatScore } from './formatting';

const baseUrl = (env.PUBLIC_API_BASE_URL || 'http://localhost:5300').replace(/\/$/, '');

export class ApiError extends Error {
  constructor(
    readonly code: string,
    message: string,
    readonly correlationId: string
  ) {
    super(message);
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${baseUrl}${path}`, {
      ...init,
      headers: { accept: 'application/json', ...init?.headers }
    });
  } catch {
    throw new ApiError('API_UNAVAILABLE', 'The platform API is unavailable.', 'unavailable');
  }
  if (!response.ok) {
    const fallback: ApiErrorResource = {
      code: `HTTP_${response.status}`,
      message: 'The platform could not complete the request.',
      details: {},
      correlationId: response.headers.get('x-correlation-id') ?? 'unavailable'
    };
    const error = (await response.json().catch(() => fallback)) as ApiErrorResource;
    throw new ApiError(error.code, error.message, error.correlationId);
  }
  return (await response.json()) as T;
}

export const api = {
  documents: () => request<DocumentResource[]>('/api/v1/documents'),
  uploadDocument: (title: string, source: string, file: File) => {
    const form = new FormData();
    form.append('title', title);
    form.append('source', source);
    form.append('file', file);
    return request<DocumentResource>('/api/v1/documents', { method: 'POST', body: form });
  },
  search: (
    query: string,
    topK: number,
    documentIds: string[],
    documentVersionIds: string[]
  ) =>
    request<SearchResponseResource>('/api/v1/search', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ query, topK, documentIds, documentVersionIds })
    }),
  citation: (citationId: string) =>
    request<CitationResource>(`/api/v1/citations/${encodeURIComponent(citationId)}`),
  evaluationStrategies: () =>
    request<EvaluationStrategyResource[]>('/api/v1/evaluations/strategies'),
  evaluationTestCases: () =>
    request<EvaluationTestCaseResource[]>('/api/v1/evaluations/test-cases'),
  createEvaluationTestCase: (query: string, relevantDocumentIds: string[], rationale: string) =>
    request<EvaluationTestCaseResource>('/api/v1/evaluations/test-cases', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ query, relevantDocumentIds, rationale })
    }),
  evaluationRuns: () =>
    request<EvaluationRunSummaryResource[]>('/api/v1/evaluations/runs'),
  evaluationRun: (runId: string) =>
    request<EvaluationRunResource>(`/api/v1/evaluations/runs/${encodeURIComponent(runId)}`),
  createEvaluationRun: (
    strategyIds: string[],
    testCaseIds: string[],
    documentVersionIds: string[],
    topK: number
  ) =>
    request<EvaluationRunResource>('/api/v1/evaluations/runs', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ strategyIds, testCaseIds, documentVersionIds, topK })
    }),
  labelEvaluationResult: (runId: string, resultId: string, relevant: boolean, notes?: string) =>
    request<EvaluationRunResource>(
      `/api/v1/evaluations/runs/${encodeURIComponent(runId)}/results/${encodeURIComponent(resultId)}/relevance`,
      {
        method: 'PATCH',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ relevant, notes })
      }
    )
};
