import { Body, Controller, Get, Headers, Param, ParseUUIDPipe, Patch, Post } from '@nestjs/common';
import { ApiCreatedResponse, ApiOkResponse, ApiTags } from '@nestjs/swagger';
import {
  CreateEvaluationRunDto,
  CreateEvaluationTestCaseDto,
  EvaluationRunResource,
  EvaluationRunSummaryResource,
  EvaluationStrategyResource,
  EvaluationTestCaseResource,
  RelevanceLabelDto,
} from './evaluation.dto';
import { EvaluationService } from './evaluation.service';

@ApiTags('retrieval evaluation')
@Controller('api/v1/evaluations')
export class EvaluationController {
  constructor(private readonly evaluation: EvaluationService) {}

  @Get('strategies')
  @ApiOkResponse({ type: [EvaluationStrategyResource] })
  strategies(@Headers('x-correlation-id') correlationId: string) {
    return this.evaluation.strategies(correlationId);
  }

  @Get('test-cases')
  @ApiOkResponse({ type: [EvaluationTestCaseResource] })
  testCases(@Headers('x-correlation-id') correlationId: string) {
    return this.evaluation.testCases(correlationId);
  }

  @Post('test-cases')
  @ApiCreatedResponse({ type: EvaluationTestCaseResource })
  createTestCase(
    @Body() dto: CreateEvaluationTestCaseDto,
    @Headers('x-correlation-id') correlationId: string,
  ) {
    return this.evaluation.createTestCase(dto, correlationId);
  }

  @Get('runs')
  @ApiOkResponse({ type: [EvaluationRunSummaryResource] })
  runs(@Headers('x-correlation-id') correlationId: string) {
    return this.evaluation.runs(correlationId);
  }

  @Post('runs')
  @ApiCreatedResponse({ type: EvaluationRunResource })
  createRun(
    @Body() dto: CreateEvaluationRunDto,
    @Headers('x-correlation-id') correlationId: string,
  ) {
    return this.evaluation.createRun(dto, correlationId);
  }

  @Get('runs/:runId')
  @ApiOkResponse({ type: EvaluationRunResource })
  run(
    @Param('runId', new ParseUUIDPipe()) runId: string,
    @Headers('x-correlation-id') correlationId: string,
  ) {
    return this.evaluation.run(runId, correlationId);
  }

  @Patch('runs/:runId/results/:resultId/relevance')
  @ApiOkResponse({ type: EvaluationRunResource })
  label(
    @Param('runId', new ParseUUIDPipe()) runId: string,
    @Param('resultId', new ParseUUIDPipe()) resultId: string,
    @Body() dto: RelevanceLabelDto,
    @Headers('x-correlation-id') correlationId: string,
  ) {
    return this.evaluation.label(runId, resultId, dto, correlationId);
  }
}
