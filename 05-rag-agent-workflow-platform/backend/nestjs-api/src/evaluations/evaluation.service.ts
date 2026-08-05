import { Injectable } from '@nestjs/common';
import {
  InternalEvaluationHit,
  InternalEvaluationRun,
  InternalEvaluationRunSummary,
  InternalEvaluationStrategy,
  InternalEvaluationTestCase,
  RagClient,
} from '../common/rag-client.service';
import { DocumentsRepository } from '../documents/documents.repository';
import {
  CreateEvaluationRunDto,
  CreateEvaluationTestCaseDto,
  EvaluationHitResource,
  EvaluationRunResource,
  EvaluationRunSummaryResource,
  EvaluationStrategyResource,
  EvaluationTestCaseResource,
  RelevanceLabelDto,
} from './evaluation.dto';

@Injectable()
export class EvaluationService {
  constructor(
    private readonly rag: RagClient,
    private readonly documents: DocumentsRepository,
  ) {}

  async strategies(correlationId: string): Promise<EvaluationStrategyResource[]> {
    return (await this.rag.evaluationStrategies(correlationId)).map(this.mapStrategy);
  }

  async testCases(correlationId: string): Promise<EvaluationTestCaseResource[]> {
    return (await this.rag.evaluationTestCases(correlationId)).map(this.mapTestCase);
  }

  async createTestCase(
    dto: CreateEvaluationTestCaseDto,
    correlationId: string,
  ): Promise<EvaluationTestCaseResource> {
    const resource = await this.rag.createEvaluationTestCase(
      {
        query: dto.query.trim(),
        relevant_document_ids: dto.relevantDocumentIds,
        rationale: dto.rationale.trim(),
      },
      correlationId,
    );
    return this.mapTestCase(resource);
  }

  async runs(correlationId: string): Promise<EvaluationRunSummaryResource[]> {
    return (await this.rag.evaluationRuns(correlationId)).map(this.mapRunSummary);
  }

  async createRun(
    dto: CreateEvaluationRunDto,
    correlationId: string,
  ): Promise<EvaluationRunResource> {
    const run = await this.rag.createEvaluationRun({
      strategy_ids: dto.strategyIds,
      test_case_ids: dto.testCaseIds,
      document_version_ids: dto.documentVersionIds,
      top_k: dto.topK,
      correlation_id: correlationId,
    });
    return this.mapRun(run);
  }

  async run(runId: string, correlationId: string): Promise<EvaluationRunResource> {
    return this.mapRun(await this.rag.evaluationRun(runId, correlationId));
  }

  async label(
    runId: string,
    resultId: string,
    dto: RelevanceLabelDto,
    correlationId: string,
  ): Promise<EvaluationRunResource> {
    const run = await this.rag.labelEvaluationResult(runId, resultId, {
      relevant: dto.relevant,
      notes: dto.notes?.trim(),
      correlation_id: correlationId,
    });
    return this.mapRun(run);
  }

  private readonly mapStrategy = (
    strategy: InternalEvaluationStrategy,
  ): EvaluationStrategyResource => ({
    strategyId: strategy.strategy_id,
    label: strategy.label,
    description: strategy.description,
    chunkSize: strategy.chunk_size,
    overlap: strategy.overlap,
    boundary: strategy.boundary,
  });

  private readonly mapTestCase = (
    testCase: InternalEvaluationTestCase,
  ): EvaluationTestCaseResource => ({
    testCaseId: testCase.test_case_id,
    query: testCase.query,
    relevantDocumentIds: testCase.relevant_document_ids,
    rationale: testCase.rationale,
    createdAt: testCase.created_at,
  });

  private readonly mapRunSummary = (
    run: InternalEvaluationRunSummary,
  ): EvaluationRunSummaryResource => ({
    runId: run.run_id,
    topK: run.top_k,
    strategyCount: run.strategy_count,
    queryCount: run.query_count,
    bestStrategyId: run.best_strategy_id,
    bestRecallAtK: run.best_recall_at_k,
    createdAt: run.created_at,
  });

  private async mapRun(run: InternalEvaluationRun): Promise<EvaluationRunResource> {
    const documentIds = [
      ...new Set(
        run.strategies.flatMap((strategy) =>
          strategy.queries.flatMap((query) => query.results.map((hit) => hit.document_id)),
        ),
      ),
    ];
    const metadata = await this.documents.metadata(documentIds);
    return {
      runId: run.run_id,
      status: run.status,
      topK: run.top_k,
      strategyIds: run.strategy_ids,
      testCaseIds: run.test_case_ids,
      documentVersionIds: run.document_version_ids,
      embeddingVersion: run.embedding_version,
      scoreSemantics: run.score_semantics,
      metricSemantics: run.metric_semantics,
      strategies: run.strategies.map((strategy) => ({
        metrics: {
          strategyId: strategy.metrics.strategy_id,
          strategyLabel: strategy.metrics.strategy_label,
          queryCount: strategy.metrics.query_count,
          chunkCount: strategy.metrics.chunk_count,
          precisionAtK: strategy.metrics.precision_at_k,
          recallAtK: strategy.metrics.recall_at_k,
          hitRate: strategy.metrics.hit_rate,
          meanReciprocalRank: strategy.metrics.mean_reciprocal_rank,
          errorCount: strategy.metrics.error_count,
        },
        queries: strategy.queries.map((query) => ({
          testCaseId: query.test_case_id,
          query: query.query,
          expectedDocumentIds: query.expected_document_ids,
          precisionAtK: query.precision_at_k,
          recallAtK: query.recall_at_k,
          hit: query.hit,
          reciprocalRank: query.reciprocal_rank,
          results: query.results.map((hit) => this.mapHit(hit, metadata)),
        })),
      })),
      createdAt: run.created_at,
      completedAt: run.completed_at,
      elapsedMs: run.elapsed_ms,
      correlationId: run.correlation_id,
    };
  }

  private mapHit(
    hit: InternalEvaluationHit,
    metadata: Map<string, { title: string; source: string }>,
  ): EvaluationHitResource {
    const document = metadata.get(hit.document_id);
    return {
      resultId: hit.result_id,
      rank: hit.rank,
      score: hit.score,
      documentId: hit.document_id,
      documentVersionId: hit.document_version_id,
      chunkId: hit.chunk_id,
      title: document?.title ?? 'Unavailable document',
      source: document?.source ?? 'Provenance unavailable',
      snippet: hit.snippet,
      locator: hit.locator,
      relevant: hit.relevant,
      relevanceSource: hit.relevance_source,
      relevanceNotes: hit.relevance_notes,
    };
  }
}
