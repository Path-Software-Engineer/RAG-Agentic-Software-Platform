import { firstValueFrom, take } from 'rxjs';
import { AgentsService } from '../src/agents/agents.service';
import { CreateAgentRunDto } from '../src/agents/agent.dto';
import { RagClient } from '../src/common/rag-client.service';

const internalRun = {
  run_id: '00000000-0000-4000-8000-000000000801',
  thread_id: '00000000-0000-4000-8000-000000000802',
  workflow_id: 'bounded-research-v1',
  status: 'completed' as const,
  outcome: 'answered' as const,
  goal: 'What does the citation policy require?',
  answer: 'Retrieved one bounded citation.',
  allowed_tool_names: ['semantic_search'],
  document_version_ids: ['00000000-0000-4000-8000-000000000803'],
  budget: {
    max_steps: 8,
    max_tool_calls: 3,
    overall_timeout_ms: 8000,
    per_tool_timeout_ms: 3000,
  },
  usage: { steps: 4, tool_calls: 1, elapsed_ms: 12.5 },
  citations: [
    {
      citation_id: '00000000-0000-4000-8000-000000000804',
      document_id: '00000000-0000-4000-8000-000000000805',
      document_version_id: '00000000-0000-4000-8000-000000000803',
      chunk_id: '00000000-0000-4000-8000-000000000806',
      rank: 1,
      score: 0.74,
      snippet: 'Every answer must preserve citation provenance.',
    },
  ],
  idempotency_key: 'agent-test-0001',
  correlation_id: '00000000-0000-4000-8000-000000000807',
  created_at: '2026-08-05T12:00:00Z',
  started_at: '2026-08-05T12:00:00Z',
  completed_at: '2026-08-05T12:00:01Z',
  error_code: null,
};

describe('AgentsService', () => {
  it('maps the governed run without exposing private reasoning', async () => {
    const rag = {
      createAgentRun: jest.fn().mockResolvedValue(internalRun),
    } as unknown as RagClient;
    const service = new AgentsService(rag);
    const dto = new CreateAgentRunDto();
    dto.goal = internalRun.goal;
    dto.idempotencyKey = internalRun.idempotency_key;

    const result = await service.create(dto, internalRun.correlation_id);

    expect(result.runId).toBe(internalRun.run_id);
    expect(result.citations).toHaveLength(1);
    expect(result.usage).toEqual({ steps: 4, toolCalls: 1, elapsedMs: 12.5 });
    expect(JSON.stringify(result)).not.toContain('reasoning');
  });

  it('replays SSE events strictly after the supplied cursor', async () => {
    const event = {
      event_id: '00000000-0000-4000-8000-000000000808',
      run_id: internalRun.run_id,
      sequence_number: 6,
      event_type: 'run_completed',
      node_id: 'finalize',
      payload: { outcome: 'answered' },
      timestamp: '2026-08-05T12:00:01Z',
    };
    const rag = {
      agentEvents: jest.fn().mockResolvedValue([event]),
    } as unknown as RagClient;
    const service = new AgentsService(rag);

    const message = await firstValueFrom(
      service.stream(internalRun.run_id, internalRun.correlation_id, 5).pipe(take(1)),
    );

    expect(rag.agentEvents).toHaveBeenCalledWith(
      internalRun.run_id,
      5,
      internalRun.correlation_id,
    );
    expect(message.id).toBe('6');
    expect(message.type).toBe('run_completed');
  });
});
