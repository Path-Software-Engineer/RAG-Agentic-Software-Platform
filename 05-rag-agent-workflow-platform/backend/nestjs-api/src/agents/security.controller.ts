import { Controller, Headers, Post } from '@nestjs/common';
import { ApiOkResponse, ApiTags } from '@nestjs/swagger';
import { SecurityEvaluationResource } from './agent.dto';
import { AgentsService } from './agents.service';

@ApiTags('security')
@Controller('api/v1/security')
export class SecurityController {
  constructor(private readonly agents: AgentsService) {}

  @Post('evaluations')
  @ApiOkResponse({ type: SecurityEvaluationResource })
  evaluate(@Headers('x-correlation-id') correlationId: string) {
    return this.agents.securityEvaluation(correlationId);
  }
}
