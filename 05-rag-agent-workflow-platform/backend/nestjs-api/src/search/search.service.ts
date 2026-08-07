import { Injectable } from '@nestjs/common';
import { ApplicationError } from '../common/error.filter';
import { RagClient } from '../common/rag-client.service';
import { DocumentsRepository } from '../documents/documents.repository';
import { CitationResource, SearchRequestDto, SearchResponseResource } from './search.dto';

@Injectable()
export class SearchService {
  constructor(
    private readonly rag: RagClient,
    private readonly documents: DocumentsRepository,
  ) {}

  async search(dto: SearchRequestDto, correlationId: string): Promise<SearchResponseResource> {
    const response = await this.rag.search({
      query: dto.query.trim(),
      top_k: dto.topK,
      document_ids: dto.documentIds,
      document_version_ids: dto.documentVersionIds,
      correlation_id: correlationId,
    });
    const metadata = await this.documents.metadata(
      [...new Set(response.results.map((result) => result.document_id))],
    );
    return {
      query: response.query,
      topK: response.top_k,
      embeddingVersionId: response.embedding_version_id,
      scoreSemantics: response.score_semantics,
      elapsedMs: response.elapsed_ms,
      correlationId: response.correlation_id,
      results: response.results.map((result) => {
        const document = metadata.get(result.document_id);
        if (!document) {
          throw new ApplicationError('SEARCH_PROVENANCE_BROKEN', 'A result has no public document.', 502);
        }
        return {
          rank: result.rank,
          score: result.score,
          documentId: result.document_id,
          documentVersionId: result.document_version_id,
          chunkId: result.chunk_id,
          citationId: result.citation_id,
          title: document.title,
          source: document.source,
          snippet: result.snippet,
          locator: result.locator,
        };
      }),
    };
  }

  async citation(citationId: string, correlationId: string): Promise<CitationResource> {
    const evidence = await this.rag.citation(citationId, correlationId);
    const metadata = await this.documents.metadata([evidence.document_id]);
    const document = metadata.get(evidence.document_id);
    if (!document) {
      throw new ApplicationError('CITATION_PROVENANCE_BROKEN', 'Citation document was not found.', 502);
    }
    return {
      citationId: evidence.citation_id,
      documentId: evidence.document_id,
      documentVersionId: evidence.document_version_id,
      chunkId: evidence.chunk_id,
      title: document.title,
      source: document.source,
      score: evidence.score,
      snippet: evidence.snippet,
      content: evidence.content,
      locator: evidence.locator,
      correlationId,
    };
  }
}
