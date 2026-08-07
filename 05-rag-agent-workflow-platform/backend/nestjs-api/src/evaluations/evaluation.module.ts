import { Module } from '@nestjs/common';
import { RagClient } from '../common/rag-client.service';
import { DocumentsModule } from '../documents/documents.module';
import { EvaluationController } from './evaluation.controller';
import { EvaluationService } from './evaluation.service';

@Module({
  imports: [DocumentsModule],
  controllers: [EvaluationController],
  providers: [EvaluationService, RagClient],
})
export class EvaluationModule {}
