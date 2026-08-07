import { Injectable, MessageEvent } from '@nestjs/common';
import { Observable } from 'rxjs';
import { RagClient } from '../common/rag-client.service';
import {
  AgentRunResource,
  AgentRunSummaryResource,
  AgentTraceEventResource,
  AgentTraceResource,
  CreateAgentRunDto,
  SecurityEvaluationResource,
  ToolDefinitionResource,
} from './agent.dto';

@Injectable()
export class AgentsService {
  constructor(private readonly rag: RagClient) {}

  async tools(correlationId: string): Promise<ToolDefinitionResource[]> {
    return (await this.rag.agentTools(correlationId)).map((item) => ({
      name: item.name,
      description: item.description,
      permission: item.permission,
      inputSchema: item.input_schema,
      timeoutMs: item.timeout_ms,
      maxResultBytes: item.max_result_bytes,
      readOnly: true,
    }));
  }

  async create(dto: CreateAgentRunDto, correlationId: string): Promise<AgentRunResource> {
    const run = await this.rag.createAgentRun({
      goal: dto.goal.trim(),
      workflow_id: dto.workflowId,
      document_version_ids: dto.documentVersionIds,
      allowed_tool_names: dto.allowedToolNames,
      budget: {
        max_steps: dto.budget.maxSteps,
        max_tool_calls: dto.budget.maxToolCalls,
        overall_timeout_ms: dto.budget.overallTimeoutMs,
        per_tool_timeout_ms: dto.budget.perToolTimeoutMs,
      },
      idempotency_key: dto.idempotencyKey,
      correlation_id: correlationId,
    });
    return this.mapRun(run);
  }

  async list(correlationId: string): Promise<AgentRunSummaryResource[]> {
    return (await this.rag.agentRuns(correlationId)).map((run) => ({
      runId: run.run_id,
      workflowId: run.workflow_id,
      status: run.status,
      outcome: run.outcome,
      goal: run.goal,
      citationCount: run.citation_count,
      createdAt: run.created_at,
      completedAt: run.completed_at,
    }));
  }

  async get(runId: string, correlationId: string): Promise<AgentRunResource> {
    return this.mapRun(await this.rag.agentRun(runId, correlationId));
  }

  async trace(runId: string, correlationId: string): Promise<AgentTraceResource> {
    const trace = await this.rag.agentTrace(runId, correlationId);
    return {
      run: this.mapRun(trace.run),
      nodes: trace.nodes.map((node) => ({
        nodeId: node.node_id,
        label: node.label,
        kind: node.kind,
      })),
      edges: trace.edges,
      steps: trace.steps.map((step) => ({
        stepId: step.step_id,
        nodeId: step.node_id,
        sequenceNumber: step.sequence_number,
        status: step.status,
        startedAt: step.started_at,
        completedAt: step.completed_at,
        durationMs: step.duration_ms,
        errorCode: step.error_code,
      })),
      toolCalls: trace.tool_calls.map((call) => ({
        toolCallId: call.tool_call_id,
        stepId: call.step_id,
        toolName: call.tool_name,
        status: call.status,
        sanitizedArguments: call.sanitized_arguments,
        sanitizedResult: call.sanitized_result,
        startedAt: call.started_at,
        completedAt: call.completed_at,
        durationMs: call.duration_ms,
        errorCode: call.error_code,
      })),
      events: trace.events.map((event) => this.mapEvent(event)),
      privateReasoningExposed: false,
    };
  }

  async cancel(runId: string, correlationId: string): Promise<AgentRunResource> {
    return this.mapRun(await this.rag.cancelAgentRun(runId, correlationId));
  }

  stream(runId: string, correlationId: string, initialCursor: number): Observable<MessageEvent> {
    return new Observable<MessageEvent>((subscriber) => {
      let cursor = initialCursor;
      let stopped = false;
      let timer: NodeJS.Timeout | undefined;

      const poll = async (): Promise<void> => {
        if (stopped) return;
        try {
          const events = await this.rag.agentEvents(runId, cursor, correlationId);
          for (const event of events) {
            cursor = Math.max(cursor, event.sequence_number);
            subscriber.next({
              id: String(event.sequence_number),
              type: event.event_type,
              data: this.mapEvent(event),
            });
          }
          if (
            events.some((event) =>
              ['run_completed', 'run_failed', 'run_cancelled'].includes(
                event.event_type,
              ),
            )
          ) {
            subscriber.complete();
            return;
          }
          if (events.length === 0) {
            const run = await this.rag.agentRun(runId, correlationId);
            if (['completed', 'failed', 'cancelled', 'blocked'].includes(run.status)) {
              subscriber.complete();
              return;
            }
            subscriber.next({
              type: 'heartbeat',
              data: { runId, afterSequence: cursor },
            });
          }
        } catch (error) {
          subscriber.error(error);
          return;
        }
        timer = setTimeout(() => void poll(), 1_000);
      };

      void poll();
      return () => {
        stopped = true;
        if (timer) clearTimeout(timer);
      };
    });
  }

  async securityEvaluation(correlationId: string): Promise<SecurityEvaluationResource> {
    const result = await this.rag.securityEvaluation(correlationId);
    return {
      evaluationId: result.evaluation_id,
      policyVersion: result.policy_version,
      scenarioCount: result.scenario_count,
      passedCount: result.passed_count,
      blockedCount: result.blocked_count,
      failedCount: result.failed_count,
      passed: result.passed,
      scenarios: result.scenarios,
      createdAt: result.created_at,
    };
  }

  private mapRun(run: Awaited<ReturnType<RagClient['agentRun']>>): AgentRunResource {
    return {
      runId: run.run_id,
      threadId: run.thread_id,
      workflowId: run.workflow_id,
      status: run.status,
      outcome: run.outcome,
      goal: run.goal,
      answer: run.answer,
      allowedToolNames: run.allowed_tool_names,
      documentVersionIds: run.document_version_ids,
      budget: {
        maxSteps: run.budget.max_steps,
        maxToolCalls: run.budget.max_tool_calls,
        overallTimeoutMs: run.budget.overall_timeout_ms,
        perToolTimeoutMs: run.budget.per_tool_timeout_ms,
      },
      usage: {
        steps: run.usage.steps,
        toolCalls: run.usage.tool_calls,
        elapsedMs: run.usage.elapsed_ms,
      },
      citations: run.citations.map((citation) => ({
        citationId: citation.citation_id,
        documentId: citation.document_id,
        documentVersionId: citation.document_version_id,
        chunkId: citation.chunk_id,
        rank: citation.rank,
        score: citation.score,
        snippet: citation.snippet,
      })),
      correlationId: run.correlation_id,
      createdAt: run.created_at,
      startedAt: run.started_at,
      completedAt: run.completed_at,
      errorCode: run.error_code,
    };
  }

  private mapEvent(event: Awaited<ReturnType<RagClient['agentEvents']>>[number]): AgentTraceEventResource {
    return {
      eventId: event.event_id,
      runId: event.run_id,
      sequenceNumber: event.sequence_number,
      eventType: event.event_type,
      nodeId: event.node_id,
      payload: event.payload,
      timestamp: event.timestamp,
    };
  }
}
