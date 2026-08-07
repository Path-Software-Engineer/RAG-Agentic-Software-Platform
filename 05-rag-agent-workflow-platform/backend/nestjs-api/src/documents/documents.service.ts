import { Injectable } from '@nestjs/common';
import { RagClient } from '../common/rag-client.service';
import { ApplicationError } from '../common/error.filter';
import { CreateDocumentDto, DocumentResource } from './document.dto';
import { validateDocument } from './document.policy';
import { DocumentsRepository } from './documents.repository';

@Injectable()
export class DocumentsService {
  constructor(
    private readonly repository: DocumentsRepository,
    private readonly rag: RagClient,
  ) {}

  async create(
    dto: CreateDocumentDto,
    file: Express.Multer.File | undefined,
    correlationId: string,
  ): Promise<DocumentResource> {
    const validated = validateDocument(file);
    const duplicate = await this.repository.findByHash(validated.contentSha256);
    if (duplicate) return this.repository.resource(duplicate, correlationId, true);

    const created = await this.repository.create(dto, validated);
    try {
      const ingestion = await this.rag.ingest({
        job_id: created.job_id,
        document_id: created.document_id,
        document_version_id: created.document_version_id,
        filename: validated.filename,
        media_type: validated.mediaType,
        content: validated.content,
        content_sha256: validated.contentSha256,
        correlation_id: correlationId,
      });
      if (!ingestion.embedding_version_id) {
        throw new ApplicationError('INGESTION_INCOMPLETE', 'Ingestion did not produce embeddings.', 502);
      }
      await this.repository.complete(
        created.job_id,
        ingestion.chunk_count,
        ingestion.embedding_version_id,
      );
      const complete = await this.repository.find(created.document_id);
      if (!complete) throw new ApplicationError('DOCUMENT_NOT_FOUND', 'Document disappeared.', 500);
      return this.repository.resource(complete, correlationId);
    } catch (error) {
      await this.repository.fail(created.job_id, 'RAG_INGESTION_FAILED');
      throw error;
    }
  }

  async list(correlationId: string): Promise<DocumentResource[]> {
    return (await this.repository.list()).map((row) => this.repository.resource(row, correlationId));
  }

  async detail(documentId: string, correlationId: string): Promise<DocumentResource> {
    const row = await this.repository.find(documentId);
    if (!row) throw new ApplicationError('DOCUMENT_NOT_FOUND', 'Document was not found.', 404);
    return this.repository.resource(row, correlationId);
  }

  async index(documentId: string, correlationId: string): Promise<DocumentResource> {
    const row = await this.repository.find(documentId);
    if (!row) throw new ApplicationError('DOCUMENT_NOT_FOUND', 'Document was not found.', 404);
    if (row.status !== 'completed') {
      throw new ApplicationError(
        'DOCUMENT_REUPLOAD_REQUIRED',
        'This failed local ingestion requires a new controlled upload.',
        409,
      );
    }
    return this.repository.resource(row, correlationId, true);
  }
}
