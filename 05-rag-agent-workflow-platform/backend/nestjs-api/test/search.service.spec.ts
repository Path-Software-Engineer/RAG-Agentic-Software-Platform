import { SearchService } from '../src/search/search.service';

describe('SearchService', () => {
  it('joins internal evidence with public document metadata without recomputing scores', async () => {
    const rag = {
      search: jest.fn().mockResolvedValue({
        query: 'citation provenance',
        top_k: 3,
        embedding_version_id: '00000000-0000-0000-0000-000000000501',
        score_semantics: 'relative',
        elapsed_ms: 1.25,
        correlation_id: '00000000-0000-0000-0000-000000000777',
        results: [
          {
            rank: 1,
            score: 0.73,
            document_id: '00000000-0000-4000-8000-000000000001',
            document_version_id: '00000000-0000-4000-8000-000000000002',
            chunk_id: '00000000-0000-4000-8000-000000000003',
            citation_id: '00000000-0000-4000-8000-000000000004',
            snippet: 'Every citation resolves.',
            locator: { start: 0, end: 24 },
          },
        ],
      }),
    };
    const documents = {
      metadata: jest.fn().mockResolvedValue(
        new Map([
          [
            '00000000-0000-4000-8000-000000000001',
            { title: 'Citation policy', source: 'Controlled corpus' },
          ],
        ]),
      ),
    };
    const service = new SearchService(rag as never, documents as never);
    const response = await service.search(
      {
        query: 'citation provenance',
        topK: 3,
        documentIds: [],
        documentVersionIds: ['00000000-0000-4000-8000-000000000002'],
      },
      '00000000-0000-0000-0000-000000000777',
    );
    expect(response.results[0]).toMatchObject({
      score: 0.73,
      title: 'Citation policy',
      citationId: '00000000-0000-4000-8000-000000000004',
    });
    expect(rag.search).toHaveBeenCalledWith(
      expect.objectContaining({
        document_version_ids: ['00000000-0000-4000-8000-000000000002'],
      }),
    );
  });
});
