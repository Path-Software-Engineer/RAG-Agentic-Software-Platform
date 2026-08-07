import { ApiProperty } from '@nestjs/swagger';
import {
  ArrayMaxSize,
  ArrayMinSize,
  IsArray,
  IsBoolean,
  IsInt,
  IsOptional,
  IsString,
  IsUUID,
  Length,
  Max,
  Min,
} from 'class-validator';

export class CreateEvaluationTestCaseDto {
  @ApiProperty({ example: 'How must retrieved instructions be treated?' })
  @IsString()
  @Length(2, 500)
  query!: string;

  @ApiProperty({ type: [String], description: 'Document-level relevance ground truth.' })
  @IsArray()
  @ArrayMinSize(1)
  @ArrayMaxSize(50)
  @IsUUID('4', { each: true })
  relevantDocumentIds!: string[];

  @ApiProperty({ example: 'The safety document contains the expected policy.' })
  @IsString()
  @Length(5, 500)
  rationale!: string;
}

export class CreateEvaluationRunDto {
  @ApiProperty({ type: [String], example: ['compact-320', 'balanced-520', 'broad-760'] })
  @IsArray()
  @ArrayMinSize(1)
  @ArrayMaxSize(5)
  @IsString({ each: true })
  strategyIds!: string[];

  @ApiProperty({ type: [String], required: false })
  @IsOptional()
  @IsArray()
  @ArrayMaxSize(100)
  @IsUUID('4', { each: true })
  testCaseIds: string[] = [];

  @ApiProperty({ type: [String], required: false })
  @IsOptional()
  @IsArray()
  @ArrayMaxSize(100)
  @IsUUID('4', { each: true })
  documentVersionIds: string[] = [];

  @ApiProperty({ default: 5, minimum: 1, maximum: 10 })
  @IsInt()
  @Min(1)
  @Max(10)
  topK = 5;
}

export class RelevanceLabelDto {
  @ApiProperty()
  @IsBoolean()
  relevant!: boolean;

  @ApiProperty({ required: false, maxLength: 500 })
  @IsOptional()
  @IsString()
  @Length(1, 500)
  notes?: string;
}

export class EvaluationStrategyResource {
  @ApiProperty() strategyId!: string;
  @ApiProperty() label!: string;
  @ApiProperty() description!: string;
  @ApiProperty() chunkSize!: number;
  @ApiProperty() overlap!: number;
  @ApiProperty() boundary!: string;
}

export class EvaluationTestCaseResource {
  @ApiProperty() testCaseId!: string;
  @ApiProperty() query!: string;
  @ApiProperty({ type: [String] }) relevantDocumentIds!: string[];
  @ApiProperty() rationale!: string;
  @ApiProperty() createdAt!: string;
}

export class EvaluationHitResource {
  @ApiProperty() resultId!: string;
  @ApiProperty() rank!: number;
  @ApiProperty() score!: number;
  @ApiProperty() documentId!: string;
  @ApiProperty() documentVersionId!: string;
  @ApiProperty() chunkId!: string;
  @ApiProperty() title!: string;
  @ApiProperty() source!: string;
  @ApiProperty() snippet!: string;
  @ApiProperty() locator!: Record<string, unknown>;
  @ApiProperty() relevant!: boolean;
  @ApiProperty() relevanceSource!: string;
  @ApiProperty({ nullable: true }) relevanceNotes!: string | null;
}

export class EvaluationQueryResource {
  @ApiProperty() testCaseId!: string;
  @ApiProperty() query!: string;
  @ApiProperty({ type: [String] }) expectedDocumentIds!: string[];
  @ApiProperty() precisionAtK!: number;
  @ApiProperty() recallAtK!: number;
  @ApiProperty() hit!: boolean;
  @ApiProperty() reciprocalRank!: number;
  @ApiProperty({ type: [EvaluationHitResource] }) results!: EvaluationHitResource[];
}

export class StrategyMetricsResource {
  @ApiProperty() strategyId!: string;
  @ApiProperty() strategyLabel!: string;
  @ApiProperty() queryCount!: number;
  @ApiProperty() chunkCount!: number;
  @ApiProperty() precisionAtK!: number;
  @ApiProperty() recallAtK!: number;
  @ApiProperty() hitRate!: number;
  @ApiProperty() meanReciprocalRank!: number;
  @ApiProperty() errorCount!: number;
}

export class EvaluationStrategyResultResource {
  @ApiProperty({ type: StrategyMetricsResource }) metrics!: StrategyMetricsResource;
  @ApiProperty({ type: [EvaluationQueryResource] }) queries!: EvaluationQueryResource[];
}

export class EvaluationRunResource {
  @ApiProperty() runId!: string;
  @ApiProperty() status!: string;
  @ApiProperty() topK!: number;
  @ApiProperty({ type: [String] }) strategyIds!: string[];
  @ApiProperty({ type: [String] }) testCaseIds!: string[];
  @ApiProperty({ type: [String] }) documentVersionIds!: string[];
  @ApiProperty() embeddingVersion!: string;
  @ApiProperty() scoreSemantics!: string;
  @ApiProperty() metricSemantics!: string;
  @ApiProperty({ type: [EvaluationStrategyResultResource] })
  strategies!: EvaluationStrategyResultResource[];
  @ApiProperty() createdAt!: string;
  @ApiProperty() completedAt!: string;
  @ApiProperty() elapsedMs!: number;
  @ApiProperty() correlationId!: string;
}

export class EvaluationRunSummaryResource {
  @ApiProperty() runId!: string;
  @ApiProperty() topK!: number;
  @ApiProperty() strategyCount!: number;
  @ApiProperty() queryCount!: number;
  @ApiProperty() bestStrategyId!: string;
  @ApiProperty() bestRecallAtK!: number;
  @ApiProperty() createdAt!: string;
}
