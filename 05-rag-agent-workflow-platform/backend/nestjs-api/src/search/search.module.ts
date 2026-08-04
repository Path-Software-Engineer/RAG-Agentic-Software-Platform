import { Module } from '@nestjs/common';
import { RagClient } from '../common/rag-client.service';
import { DocumentsModule } from '../documents/documents.module';
import { SearchController } from './search.controller';
import { SearchService } from './search.service';

@Module({
  imports: [DocumentsModule],
  controllers: [SearchController],
  providers: [SearchService, RagClient],
})
export class SearchModule {}
