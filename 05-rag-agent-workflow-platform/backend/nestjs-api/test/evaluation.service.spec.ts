import { EvaluationService } from '../src/evaluations/evaluation.service';

const RUN_ID = '00000000-0000-4000-8000-000000000601';
const RESULT_ID = '00000000-0000-4000-8000-000000000602';
const DOCUMENT_ID = '00000000-0000-4000-8000-000000000603';

function internalRun() {
  return {
    run_id: RUN_ID,
    status: 'completed' as const,
    top_k: 3,
    strategy_ids: ['balanced-520'],
    test_case_ids: ['00000000-0000-4000-8000-000000000604'],
    document_version_ids: ['00000000-0000-4000-8000-000000000605'],
    embedding_version: 'local:deterministic-hash-v1:128:canonical-text-v1',
    score_semantics: 'cosine similarity; not confidence',
    metric_semantics: 'macro average over explicit relevance judgments',
    strategies: [
      {
        metrics: {
          strategy_id: 'balanced-520',
          strategy_label: 'Balanced context',
          query_count: 1,
          chunk_count: 4,
          precision_at_k: 0.333333,
          recall_at_k: 1,
          hit_rate: 1,
          mean_reciprocal_rank: 1,
          error_count: 0,
        },
        queries: [
          {
            test_case_id: '00000000-0000-4000-8000-000000000604',
            query: 'How is evidence preserved?',
            expected_document_ids: [DOCUMENT_ID],
            precision_at_k: 0.333333,
            recall_at_k: 1,
            hit: true,
            reciprocal_rank: 1,
            results: [
              {
                result_id: RESULT_ID,
                rank: 1,
                score: 0.781,
                document_id: DOCUMENT_ID,
                document_version_id: '00000000-0000-4000-8000-000000000605',
                chunk_id: '00000000-0000-4000-8000-000000000606',
                snippet: 'Every citation preserves durable evidence.',
                locator: { start: 0, end: 44 },
                relevant: true,
                relevance_source: 'expected-set' as const,
                relevance_notes: null,
              },
            ],
          },
        ],
      },
    ],
    created_at: '2026-08-04T10:00:00Z',
    completed_at: '2026-08-04T10:00:01Z',
    elapsed_ms: 15.2,
    correlation_id: '00000000-0000-4000-8000-000000000607',
  };
}

describe('EvaluationService', () => {
  it('maps immutable evaluation evidence without recomputing metrics or similarity', async () => {
    const rag = { createEvaluationRun: jest.fn().mockResolvedValue(internalRun()) };
    const documents = {
      metadata: jest.fn().mockResolvedValue(
        new Map([[DOCUMENT_ID, { title: 'Citation policy', source: 'Controlled corpus' }]]),
      ),
    };
    const service = new EvaluationService(rag as never, documents as never);

    const response = await service.createRun(
      {
        strategyIds: ['balanced-520'],
        testCaseIds: ['00000000-0000-4000-8000-000000000604'],
        documentVersionIds: ['00000000-0000-4000-8000-000000000605'],
        topK: 3,
      },
      '00000000-0000-4000-8000-000000000607',
    );

    expect(response.strategies[0].metrics).toMatchObject({
      recallAtK: 1,
      precisionAtK: 0.333333,
      meanReciprocalRank: 1,
    });
    expect(response.strategies[0].queries[0].results[0]).toMatchObject({
      resultId: RESULT_ID,
      score: 0.781,
      title: 'Citation policy',
      relevant: true,
    });
    expect(rag.createEvaluationRun).toHaveBeenCalledWith(
      expect.objectContaining({ strategy_ids: ['balanced-520'], top_k: 3 }),
    );
  });

  it('forwards manual relevance labels with the public correlation identifier', async () => {
    const rag = { labelEvaluationResult: jest.fn().mockResolvedValue(internalRun()) };
    const documents = { metadata: jest.fn().mockResolvedValue(new Map()) };
    const service = new EvaluationService(rag as never, documents as never);

    await service.label(
      RUN_ID,
      RESULT_ID,
      { relevant: false, notes: 'Reviewed manually.' },
      '00000000-0000-4000-8000-000000000607',
    );

    expect(rag.labelEvaluationResult).toHaveBeenCalledWith(RUN_ID, RESULT_ID, {
      relevant: false,
      notes: 'Reviewed manually.',
      correlation_id: '00000000-0000-4000-8000-000000000607',
    });
  });
});
