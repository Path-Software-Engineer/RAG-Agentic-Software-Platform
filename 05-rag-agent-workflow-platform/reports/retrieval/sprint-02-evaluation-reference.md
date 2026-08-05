# Sprint 2 Retrieval Evaluation Reference

## Controlled experiment

- corpus: the four synthetic documents in `data/samples`;
- ground truth: three document-level query judgments created by `seed-evaluation-demo.ps1`;
- strategies: compact 320/48, balanced 520/80, broad 760/120;
- cutoff: Top 3 in the reference demo;
- embedding: deterministic-hash-v1, 128 dimensions;
- metrics: macro Precision@3, Recall@3, Hit Rate, MRR, chunk count, and incomplete-recall count.

## Result status

No metric values are recorded in this source-controlled report before the Docker-backed E2E is executed from the normal terminal. The run itself persists exact values in `rag.evaluation_runs`; the dashboard exposes that snapshot and its evidence. This prevents a static document from claiming results that were not executed in the current environment.

## Interpretation

Any observed leader is conditional on this corpus, relevance set, embedding version, strategy versions, and cutoff. Similarity is not confidence. Manual relevance labels are auditable reviewer judgments. The reference does not demonstrate production retrieval quality or external generalization.
