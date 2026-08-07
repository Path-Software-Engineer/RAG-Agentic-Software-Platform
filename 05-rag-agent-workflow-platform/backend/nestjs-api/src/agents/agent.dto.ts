import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import {
  ArrayMaxSize,
  ArrayMinSize,
  IsArray,
  IsIn,
  IsInt,
  IsOptional,
  IsString,
  IsUUID,
  Length,
  Matches,
  Max,
  Min,
  ValidateNested,
} from 'class-validator';
import { Type } from 'class-transformer';

export const agentStatuses = [
  'queued',
  'running',
  'waiting',
  'completed',
  'failed',
  'cancelled',
  'blocked',
] as const;

export class AgentBudgetDto {
  @ApiProperty({ default: 8, minimum: 4, maximum: 16 })
  @IsInt()
  @Min(4)
  @Max(16)
  maxSteps = 8;

  @ApiProperty({ default: 3, minimum: 1, maximum: 6 })
  @IsInt()
  @Min(1)
  @Max(6)
  maxToolCalls = 3;

  @ApiProperty({ default: 8000, minimum: 500, maximum: 20000 })
  @IsInt()
  @Min(500)
  @Max(20_000)
  overallTimeoutMs = 8_000;

  @ApiProperty({ default: 3000, minimum: 250, maximum: 8000 })
  @IsInt()
  @Min(250)
  @Max(8_000)
  perToolTimeoutMs = 3_000;
}

export class CreateAgentRunDto {
  @ApiProperty({ example: 'How should retrieved instructions be treated?' })
  @IsString()
  @Length(3, 500)
  goal!: string;

  @ApiProperty({ default: 'bounded-research-v1' })
  @IsIn(['bounded-research-v1'])
  workflowId = 'bounded-research-v1';

  @ApiProperty({ type: [String], required: false })
  @IsOptional()
  @IsArray()
  @ArrayMaxSize(50)
  @IsUUID('4', { each: true })
  documentVersionIds: string[] = [];

  @ApiProperty({ type: [String], default: ['semantic_search'] })
  @IsArray()
  @ArrayMinSize(1)
  @ArrayMaxSize(3)
  @IsIn(['semantic_search', 'document_lookup', 'evaluation_lookup'], { each: true })
  allowedToolNames: string[] = ['semantic_search'];

  @ApiPropertyOptional({ type: AgentBudgetDto })
  @IsOptional()
  @ValidateNested()
  @Type(() => AgentBudgetDto)
  budget: AgentBudgetDto = new AgentBudgetDto();

  @ApiProperty({ example: 'demo-run-2026-08-05-001' })
  @IsString()
  @Length(8, 120)
  @Matches(/^[A-Za-z0-9._:-]+$/)
  idempotencyKey!: string;
}

export class AgentRunResource {
  @ApiProperty() runId!: string;
  @ApiProperty() threadId!: string;
  @ApiProperty() workflowId!: string;
  @ApiProperty({ enum: agentStatuses }) status!: string;
  @ApiProperty({ nullable: true }) outcome!: string | null;
  @ApiProperty() goal!: string;
  @ApiProperty({ nullable: true }) answer!: string | null;
  @ApiProperty({ type: [String] }) allowedToolNames!: string[];
  @ApiProperty({ type: [String] }) documentVersionIds!: string[];
  @ApiProperty() budget!: Record<string, number>;
  @ApiProperty() usage!: Record<string, number>;
  @ApiProperty({ type: [Object] }) citations!: Array<Record<string, unknown>>;
  @ApiProperty() correlationId!: string;
  @ApiProperty() createdAt!: string;
  @ApiProperty({ nullable: true }) startedAt!: string | null;
  @ApiProperty({ nullable: true }) completedAt!: string | null;
  @ApiProperty({ nullable: true }) errorCode!: string | null;
}

export class AgentRunSummaryResource {
  @ApiProperty() runId!: string;
  @ApiProperty() workflowId!: string;
  @ApiProperty({ enum: agentStatuses }) status!: string;
  @ApiProperty({ nullable: true }) outcome!: string | null;
  @ApiProperty() goal!: string;
  @ApiProperty() citationCount!: number;
  @ApiProperty() createdAt!: string;
  @ApiProperty({ nullable: true }) completedAt!: string | null;
}

export class AgentTraceEventResource {
  @ApiProperty() eventId!: string;
  @ApiProperty() runId!: string;
  @ApiProperty() sequenceNumber!: number;
  @ApiProperty() eventType!: string;
  @ApiProperty({ nullable: true }) nodeId!: string | null;
  @ApiProperty() payload!: Record<string, unknown>;
  @ApiProperty() timestamp!: string;
}

export class AgentTraceResource {
  @ApiProperty({ type: AgentRunResource }) run!: AgentRunResource;
  @ApiProperty({ type: [Object] }) nodes!: Array<Record<string, unknown>>;
  @ApiProperty({ type: [Object] }) edges!: Array<Record<string, unknown>>;
  @ApiProperty({ type: [Object] }) steps!: Array<Record<string, unknown>>;
  @ApiProperty({ type: [Object] }) toolCalls!: Array<Record<string, unknown>>;
  @ApiProperty({ type: [AgentTraceEventResource] }) events!: AgentTraceEventResource[];
  @ApiProperty({ default: false }) privateReasoningExposed!: false;
}

export class ToolDefinitionResource {
  @ApiProperty() name!: string;
  @ApiProperty() description!: string;
  @ApiProperty() permission!: string;
  @ApiProperty() inputSchema!: Record<string, unknown>;
  @ApiProperty() timeoutMs!: number;
  @ApiProperty() maxResultBytes!: number;
  @ApiProperty({ default: true }) readOnly!: true;
}

export class SecurityEvaluationResource {
  @ApiProperty() evaluationId!: string;
  @ApiProperty() policyVersion!: string;
  @ApiProperty() scenarioCount!: number;
  @ApiProperty() passedCount!: number;
  @ApiProperty() blockedCount!: number;
  @ApiProperty() failedCount!: number;
  @ApiProperty() passed!: boolean;
  @ApiProperty({ type: [Object] }) scenarios!: Array<Record<string, unknown>>;
  @ApiProperty() createdAt!: string;
}
