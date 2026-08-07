const { mkdirSync, writeFileSync } = require('node:fs');
const { resolve } = require('node:path');
const { NestFactory } = require('@nestjs/core');
const { DocumentBuilder, SwaggerModule } = require('@nestjs/swagger');
const { AppModule } = require('../dist/app.module');

async function main() {
  const app = await NestFactory.create(AppModule, { logger: false, abortOnError: false });
  const configuration = new DocumentBuilder()
    .setTitle('RAG & Agent Workflow Platform API')
    .setDescription(
      'Public document, retrieval evaluation and governed Agent Workflow Trace Viewer contract.',
    )
    .setVersion('1.0.0')
    .build();
  const document = SwaggerModule.createDocument(app, configuration);
  const outputDirectory = resolve(__dirname, '../../../packages/contracts/openapi');
  mkdirSync(outputDirectory, { recursive: true });
  writeFileSync(resolve(outputDirectory, 'public-v1.json'), `${JSON.stringify(document, null, 2)}\n`);
  await app.close();
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
