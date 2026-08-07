# Trace Contract — Agent Workflow 1.0

A trace is an operational record of observable execution. It is not chain-of-thought and must not be presented as causal model explanation.

The trace resource contains:

- the durable run and terminal outcome;
- the declared workflow nodes and edges;
- the actually executed ordered steps;
- sanitized allowlisted tool calls;
- ordered trace events;
- resolvable citations;
- `privateReasoningExposed: false`.

The declared graph for `bounded-research-v1` is:

```text
policy_check --allowed--> retrieve_evidence --> assess_evidence --> finalize
      \--blocked-----------------------------------------------> finalize
```

An execution path is derived from persisted steps, not inferred by the browser. Durations are operational observations. Similarity scores are ranking signals. A blocked path contains no tool calls. A run is terminal only with one explicit outcome.

Retention policy for the local release:

- runs, steps, calls, events and checkpoints remain in PostgreSQL until the project volume is intentionally removed;
- Redis events expire after one hour and are capped at 500 entries per run;
- no document body or secret is duplicated into the trace.
