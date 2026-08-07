# Week 1 Exploration — Evaluation contract

Questions covered the relevance unit, test-set ownership, comparable experiment inputs, metric semantics, and persistence. Document-level binary relevance was chosen as the smallest auditable ground truth. Passage-level graded relevance and external benchmark datasets were deferred.

The experiment contract freezes strategy IDs, test-case IDs, document-version IDs, cutoff, embedding behavior, and correlation ID. Metrics cannot be interpreted outside that disclosed boundary.
