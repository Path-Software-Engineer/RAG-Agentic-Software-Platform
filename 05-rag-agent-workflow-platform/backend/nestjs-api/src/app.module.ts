import { MiddlewareConsumer, Module, NestModule } from '@nestjs/common';
import { CorrelationMiddleware } from './common/correlation.middleware';
import { CommonModule } from './common/common.module';
import { DocumentsModule } from './documents/documents.module';
import { HealthController } from './health.controller';
import { SearchModule } from './search/search.module';

@Module({
  imports: [CommonModule, DocumentsModule, SearchModule],
  controllers: [HealthController],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer): void {
    consumer.apply(CorrelationMiddleware).forRoutes('*');
  }
}
