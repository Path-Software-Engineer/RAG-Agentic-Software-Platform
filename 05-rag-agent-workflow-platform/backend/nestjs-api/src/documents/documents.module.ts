import { Module } from '@nestjs/common';
import { RagClient } from '../common/rag-client.service';
import { DocumentsController } from './documents.controller';
import { DocumentsRepository } from './documents.repository';
import { DocumentsService } from './documents.service';

@Module({
  controllers: [DocumentsController],
  providers: [DocumentsRepository, DocumentsService, RagClient],
  exports: [DocumentsRepository],
})
export class DocumentsModule {}
