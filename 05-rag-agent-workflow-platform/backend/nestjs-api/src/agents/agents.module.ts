import { Module } from '@nestjs/common';
import { CommonModule } from '../common/common.module';
import { RagClient } from '../common/rag-client.service';
import { AgentsController } from './agents.controller';
import { AgentsService } from './agents.service';
import { SecurityController } from './security.controller';

@Module({
  imports: [CommonModule],
  controllers: [AgentsController, SecurityController],
  providers: [AgentsService, RagClient],
})
export class AgentsModule {}
