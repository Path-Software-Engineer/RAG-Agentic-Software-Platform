import {
  Body,
  Controller,
  Get,
  Headers,
  MessageEvent,
  Param,
  ParseUUIDPipe,
  Post,
  Sse,
} from '@nestjs/common';
import { ApiOkResponse, ApiTags } from '@nestjs/swagger';
import { Observable } from 'rxjs';
import {
  AgentRunResource,
  AgentRunSummaryResource,
  AgentTraceResource,
  CreateAgentRunDto,
  ToolDefinitionResource,
} from './agent.dto';
import { AgentsService } from './agents.service';

@ApiTags('agents')
@Controller('api/v1/agents')
export class AgentsController {
  constructor(private readonly agents: AgentsService) {}

  @Get('tools')
  @ApiOkResponse({ type: [ToolDefinitionResource] })
  tools(@Headers('x-correlation-id') correlationId: string) {
    return this.agents.tools(correlationId);
  }

  @Post('runs')
  @ApiOkResponse({ type: AgentRunResource })
  create(
    @Body() dto: CreateAgentRunDto,
    @Headers('x-correlation-id') correlationId: string,
  ) {
    return this.agents.create(dto, correlationId);
  }

  @Get('runs')
  @ApiOkResponse({ type: [AgentRunSummaryResource] })
  list(@Headers('x-correlation-id') correlationId: string) {
    return this.agents.list(correlationId);
  }

  @Get('runs/:runId')
  @ApiOkResponse({ type: AgentRunResource })
  get(
    @Param('runId', new ParseUUIDPipe()) runId: string,
    @Headers('x-correlation-id') correlationId: string,
  ) {
    return this.agents.get(runId, correlationId);
  }

  @Get('runs/:runId/trace')
  @ApiOkResponse({ type: AgentTraceResource })
  trace(
    @Param('runId', new ParseUUIDPipe()) runId: string,
    @Headers('x-correlation-id') correlationId: string,
  ) {
    return this.agents.trace(runId, correlationId);
  }

  @Sse('runs/:runId/events')
  events(
    @Param('runId', new ParseUUIDPipe()) runId: string,
    @Headers('x-correlation-id') correlationId: string,
    @Headers('last-event-id') lastEventId?: string,
  ): Observable<MessageEvent> {
    const parsed = Number.parseInt(lastEventId ?? '0', 10);
    const cursor = Number.isFinite(parsed) && parsed >= 0 ? parsed : 0;
    return this.agents.stream(runId, correlationId, cursor);
  }

  @Post('runs/:runId/cancel')
  @ApiOkResponse({ type: AgentRunResource })
  cancel(
    @Param('runId', new ParseUUIDPipe()) runId: string,
    @Headers('x-correlation-id') correlationId: string,
  ) {
    return this.agents.cancel(runId, correlationId);
  }
}
