# Sprint 2 Demo Script

1. Start the platform and seed the Sprint 1 corpus.
2. Run `scripts/seed-evaluation-demo.ps1` or open `/evaluation` and create the three controlled test cases.
3. Explain that the expected documents and rationale form the visible ground truth.
4. Run all three strategies at Top 3 using the same corpus versions.
5. Compare Recall@3 visually, then use the table for exact Precision@3, Recall@3, Hit Rate, MRR, chunks, and errors.
6. Expand an incomplete-recall query and inspect rank, similarity, source, and snippet.
7. Apply a relevance label and show the recalculated snapshot.
8. Close with the evidence boundary: the test set is synthetic and the metrics do not establish production readiness.
