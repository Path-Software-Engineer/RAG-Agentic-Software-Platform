import { Injectable } from '@nestjs/common';
import { PoolClient } from 'pg';
import { DatabaseService } from '../common/database.service';
import { CreateDocumentDto, DocumentResource } from './document.dto';
import { ValidatedDocument } from './document.policy';

interface DocumentRow {
  document_id: string;
  document_version_id: string;
  job_id: string;
  title: string;
  source: string;
  filename: string;
  status: string;
  chunk_count: number;
  embedding_version_id: string | null;
  created_at: Date;
}

@Injectable()
export class DocumentsRepository {
  constructor(private readonly database: DatabaseService) {}

  private readonly select = `
    SELECT d.id document_id, v.id document_version_id, j.id job_id, d.title, d.source,
           v.filename, j.status, j.chunk_count, j.embedding_version_id, d.created_at
    FROM app.documents d
    JOIN app.document_versions v ON v.document_id=d.id
    JOIN app.ingestion_jobs j ON j.document_version_id=v.id`;

  async findByHash(hash: string): Promise<DocumentRow | null> {
    const result = await this.database.query<DocumentRow>(
      `${this.select} WHERE v.content_sha256=$1 ORDER BY v.version DESC LIMIT 1`,
      [hash],
    );
    return result.rows[0] ?? null;
  }

  async create(dto: CreateDocumentDto, file: ValidatedDocument): Promise<DocumentRow> {
    return this.database.transaction(async (client: PoolClient) => {
      const document = await client.query<{ id: string; created_at: Date }>(
        'INSERT INTO app.documents(title, source) VALUES ($1, $2) RETURNING id, created_at',
        [dto.title.trim(), dto.source.trim()],
      );
      const documentId = document.rows[0].id;
      const version = await client.query<{ id: string }>(
        `INSERT INTO app.document_versions(document_id, version, filename, media_type, byte_size, content_sha256)
         VALUES ($1, 1, $2, $3, $4, $5) RETURNING id`,
        [documentId, file.filename, file.mediaType, file.byteSize, file.contentSha256],
      );
      const documentVersionId = version.rows[0].id;
      const job = await client.query<{ id: string }>(
        `INSERT INTO app.ingestion_jobs(document_id, document_version_id, idempotency_key)
         VALUES ($1, $2, $3) RETURNING id`,
        [documentId, documentVersionId, `sha256:${file.contentSha256}`],
      );
      return {
        document_id: documentId,
        document_version_id: documentVersionId,
        job_id: job.rows[0].id,
        title: dto.title.trim(),
        source: dto.source.trim(),
        filename: file.filename,
        status: 'queued',
        chunk_count: 0,
        embedding_version_id: null,
        created_at: document.rows[0].created_at,
      };
    });
  }

  async complete(jobId: string, chunkCount: number, embeddingVersionId: string): Promise<void> {
    await this.database.transaction(async (client) => {
      const job = await client.query<{ document_id: string }>(
        `UPDATE app.ingestion_jobs SET status='completed', chunk_count=$2,
         embedding_version_id=$3, started_at=COALESCE(started_at, now()), completed_at=now()
         WHERE id=$1 RETURNING document_id`,
        [jobId, chunkCount, embeddingVersionId],
      );
      await client.query("UPDATE app.documents SET status='completed', updated_at=now() WHERE id=$1", [
        job.rows[0].document_id,
      ]);
    });
  }

  async fail(jobId: string, code: string): Promise<void> {
    await this.database.transaction(async (client) => {
      const job = await client.query<{ document_id: string }>(
        `UPDATE app.ingestion_jobs SET status='failed', error_code=$2,
         error_message='Internal ingestion failed', completed_at=now()
         WHERE id=$1 RETURNING document_id`,
        [jobId, code],
      );
      if (job.rows[0]) {
        await client.query("UPDATE app.documents SET status='failed', updated_at=now() WHERE id=$1", [
          job.rows[0].document_id,
        ]);
      }
    });
  }

  async list(): Promise<DocumentRow[]> {
    return (await this.database.query<DocumentRow>(`${this.select} ORDER BY d.created_at DESC`)).rows;
  }

  async find(documentId: string): Promise<DocumentRow | null> {
    const result = await this.database.query<DocumentRow>(
      `${this.select} WHERE d.id=$1 ORDER BY v.version DESC LIMIT 1`,
      [documentId],
    );
    return result.rows[0] ?? null;
  }

  async metadata(documentIds: string[]): Promise<Map<string, { title: string; source: string }>> {
    if (!documentIds.length) return new Map();
    const result = await this.database.query<{ id: string; title: string; source: string }>(
      'SELECT id, title, source FROM app.documents WHERE id = ANY($1::uuid[])',
      [documentIds],
    );
    return new Map(result.rows.map((row) => [row.id, { title: row.title, source: row.source }]));
  }

  resource(row: DocumentRow, correlationId: string, deduplicated = false): DocumentResource {
    return {
      documentId: row.document_id,
      documentVersionId: row.document_version_id,
      jobId: row.job_id,
      title: row.title,
      source: row.source,
      filename: row.filename,
      status: row.status,
      chunkCount: row.chunk_count,
      embeddingVersionId: row.embedding_version_id,
      createdAt: row.created_at.toISOString(),
      correlationId,
      deduplicated,
    };
  }
}
