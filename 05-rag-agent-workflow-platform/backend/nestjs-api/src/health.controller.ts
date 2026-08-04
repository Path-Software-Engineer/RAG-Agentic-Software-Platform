import { Controller, Get, ServiceUnavailableException } from '@nestjs/common';
import { ApiOkResponse, ApiTags } from '@nestjs/swagger';
import { DatabaseService } from './common/database.service';

@ApiTags('health')
@Controller()
export class HealthController {
  constructor(private readonly database: DatabaseService) {}

  @Get('healthz')
  @ApiOkResponse({ schema: { example: { status: 'ok', service: 'rag-platform-api' } } })
  async health() {
    if (!(await this.database.health())) throw new ServiceUnavailableException('pgvector unavailable');
    return { status: 'ok', service: 'rag-platform-api' };
  }
}
