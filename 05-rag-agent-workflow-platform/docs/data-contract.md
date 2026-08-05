# Data Contract — Retrieval Platform 0.2

## Canonical document and chunk

- document IDs are opaque UUIDs owned by `app`;
- document-version IDs identify immutable uploaded bytes;
- `content_sha256` supports deduplication;
- canonical UTF-8 source text is retained in `rag.document_sources` so evaluation strategies can rechunk the exact indexed version;
- chunks retain document/version IDs, order, offsets, locator, content, and chunking version.

## Embedding and score

Provider, model, dimension, preprocessing version, and creation time define an embedding version. Vectors from incompatible versions are never compared in one logical query. The reference dimension is 128. Similarity is `1 - cosine_distance`, bounded to `[-1, 1]`; it is not probability, confidence, truth, or answer correctness.

## Retrieval test case

| Field | Meaning |
|---|---|
| `test_case_id` | Stable UUID of one judgment scenario |
| `query` | Controlled retrieval question |
| `relevant_document_ids` | Document-level expected evidence set |
| `rationale` | Human-readable reason for the expected set |
| `created_at` | UTC creation time |

The ground truth is intentionally document-level for this sprint. Passage-level graded judgments remain future work.

## Evaluation strategy

The built-in versioned strategies are `compact-320` (320/48), `balanced-520` (520/80), and `broad-760` (760/120). Each uses the same natural character-window boundary algorithm and embedding adapter. The ID is part of the evidence contract.

## Metrics

- `Precision@K`: relevant returned chunks divided by K;
- `Recall@K`: unique expected documents retrieved divided by expected-document count;
- `Hit Rate`: fraction of test cases with at least one relevant hit;
- `MRR`: mean reciprocal rank of the first relevant hit;
- `error_count`: test cases whose Recall@K is below 1.

Strategy metrics are macro averages across selected test cases. Values are bounded from 0 through 1 and rounded to six decimals. They cannot be compared across different corpora, test sets, embedding versions, or cutoffs without disclosing those differences.

## Evaluation run and label audit

`rag.evaluation_runs` stores the complete JSON snapshot plus strategy IDs, test-case IDs, document versions, cutoff, status, timestamps, and correlation ID. A result ID is deterministic inside its run. `rag.relevance_labels` records the latest manual judgment, notes, correlation ID, and review time. A review recalculates the affected query and strategy metrics but preserves the original expected-document set.
