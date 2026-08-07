# Week 2 Review — Evaluation engine

FastAPI now loads canonical source versions, rechunks each strategy, embeds and ranks identical queries, calculates per-query and macro metrics, persists complete snapshots, and summarizes the observed leader under explicit tie-breaking. Unit tests cover catalog boundaries, metrics, invalid inputs, persistence summaries, and audited labels.

Evidence: `app/evaluation.py` and `tests/test_retrieval_evaluation.py`.
