import { env } from '$env/dynamic/public';
import type {
  AgentRunResource,
  AgentRunSummaryResource,
  AgentTraceResource,
  ApiErrorResource,
  CitationResource,
  DocumentResource,
  EvaluationRunResource,
  EvaluationRunSummaryResource,
  EvaluationStrategyResource,
  EvaluationTestCaseResource,
  SearchResponseResource,
  SecurityEvaluationResource,
  ToolDefinitionResource
} from './types';
export { formatLocator, formatScore } from './formatting';

const baseUrl = (env.PUBLIC_API_BASE_URL || 'http://localhost:5300').replace(/\/$/, '');

async function sha256Hex(payload: BodyInit): Promise<string> {
  let bytes: ArrayBuffer;
  if (typeof payload === 'string') {
    bytes = new TextEncoder().encode(payload).buffer as ArrayBuffer;
  } else if (payload instanceof Blob) {
    bytes = await payload.arrayBuffer();
  } else if (payload instanceof ArrayBuffer) {
    bytes = payload;
  } else if (ArrayBuffer.isView(payload)) {
    bytes = payload.buffer.slice(
      payload.byteOffset,
      payload.byteOffset + payload.byteLength
    ) as ArrayBuffer;
  } else {
    throw new ApiError(
      'PAYLOAD_HASH_UNSUPPORTED',
      'This request body cannot be prepared for the protected cloud boundary.',
      'client'
    );
  }
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return Array.from(new Uint8Array(digest), (value) => value.toString(16).padStart(2, '0')).join('');
}

function escapedMultipartValue(value: string): string {
  return value.replace(/[\r\n]/g, ' ').replace(/"/g, '%22');
}

async function documentMultipart(
  title: string,
  source: string,
  file: File
): Promise<{ body: Blob; contentType: string }> {
  const boundary = `----sf05-${crypto.randomUUID()}`;
  const contentType = `multipart/form-data; boundary=${boundary}`;
  const body = new Blob(
    [
      `--${boundary}\r\nContent-Disposition: form-data; name="title"\r\n\r\n${title}\r\n`,
      `--${boundary}\r\nContent-Disposition: form-data; name="source"\r\n\r\n${source}\r\n`,
      `--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${escapedMultipartValue(file.name)}"\r\n`,
      `Content-Type: ${file.type || 'application/octet-stream'}\r\n\r\n`,
      file,
      `\r\n--${boundary}--\r\n`
    ],
    { type: contentType }
  );
  return { body, contentType };
}

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
    const headers = new Headers(init?.headers);
    headers.set('accept', 'application/json');
    if (init?.body !== undefined && init.body !== null) {
      headers.set('x-amz-content-sha256', await sha256Hex(init.body));
    }
    response = await fetch(`${baseUrl}${path}`, {
      ...init,
      headers
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
  uploadDocument: async (title: string, source: string, file: File) => {
    const multipart = await documentMultipart(title, source, file);
    return request<DocumentResource>('/api/v1/documents', {
      method: 'POST',
      headers: { 'content-type': multipart.contentType },
      body: multipart.body
    });
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
    ),
  agentTools: () => request<ToolDefinitionResource[]>('/api/v1/agents/tools'),
  agentRuns: () => request<AgentRunSummaryResource[]>('/api/v1/agents/runs'),
  agentRun: (runId: string) =>
    request<AgentRunResource>(`/api/v1/agents/runs/${encodeURIComponent(runId)}`),
  agentTrace: (runId: string) =>
    request<AgentTraceResource>(`/api/v1/agents/runs/${encodeURIComponent(runId)}/trace`),
  createAgentRun: (payload: {
    goal: string;
    workflowId: 'bounded-research-v1';
    documentVersionIds: string[];
    allowedToolNames: string[];
    budget: {
      maxSteps: number;
      maxToolCalls: number;
      overallTimeoutMs: number;
      perToolTimeoutMs: number;
    };
    idempotencyKey: string;
  }) =>
    request<AgentRunResource>('/api/v1/agents/runs', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(payload)
    }),
  cancelAgentRun: (runId: string) =>
    request<AgentRunResource>(`/api/v1/agents/runs/${encodeURIComponent(runId)}/cancel`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: '{}'
    }),
  securityEvaluation: () =>
    request<SecurityEvaluationResource>('/api/v1/security/evaluations', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: '{}'
    })
};

export function agentEventsUrl(runId: string) {
  return `${baseUrl}/api/v1/agents/runs/${encodeURIComponent(runId)}/events`;
}
