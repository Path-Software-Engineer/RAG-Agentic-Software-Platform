# Sprint 1 Reference Search Decision

The controlled corpus is intentionally too small for a meaningful ANN benchmark. Exact cosine search is therefore the only enabled path and acts as the correctness oracle.

An approximate index will be considered only when a versioned benchmark can report dataset size, query count, recall against exact search, p50/p95 latency, parameters, hardware, and repeated runs. Sprint 1 makes no latency or scalability claim.
