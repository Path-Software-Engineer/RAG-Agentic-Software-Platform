import { ValidationPipe } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AppModule } from './app.module';
import { ApiExceptionFilter } from './common/error.filter';

async function bootstrap(): Promise<void> {
  const app = await NestFactory.create(AppModule, { logger: ['log', 'warn', 'error'] });
  app.useGlobalPipes(
    new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }),
  );
  app.useGlobalFilters(new ApiExceptionFilter());
  app.enableCors({
    origin: (process.env.CORS_ORIGINS ?? 'http://localhost:5173').split(','),
    methods: ['GET', 'POST', 'PATCH'],
    exposedHeaders: ['x-correlation-id'],
  });

  const swagger = new DocumentBuilder()
    .setTitle('RAG & Agent Workflow Platform API')
    .setDescription(
      'Sprint 2 public document, semantic-search, citation and retrieval-evaluation contract.',
    )
    .setVersion('0.2.0')
    .build();
  const document = SwaggerModule.createDocument(app, swagger);
  SwaggerModule.setup('api/docs', app, document);
  app.getHttpAdapter().get('/api/openapi.json', (_request: unknown, response: { json: (value: unknown) => void }) => response.json(document));

  await app.listen(Number(process.env.PORT ?? 3000), '0.0.0.0');
}

void bootstrap();
