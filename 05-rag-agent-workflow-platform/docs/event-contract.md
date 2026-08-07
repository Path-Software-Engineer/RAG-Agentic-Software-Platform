# Event Contract — Agent Trace 1.0

Every persisted event conforms to `packages/contracts/schemas/agent-trace-event.schema.json`.

Required fields are `event_id`, `run_id`, `sequence_number`, `event_type`, `payload`, and UTC `timestamp`. `sequence_number` starts at 1 and is unique per run. `node_id` is present only when an event belongs to a graph node.

Supported event types:

- `run_started`;
- `step_started`, `step_completed`, `step_failed`;
- `tool_called`, `tool_completed`, `tool_failed`;
- `policy_blocked`;
- `run_completed`, `run_failed`, `run_cancelled`.

Payloads may contain IDs, status, policy/error codes, durations, counts and sanitized bounded tool data. They must not contain credentials, bearer tokens, email addresses, full documents, system prompts or private reasoning.

PostgreSQL stores the canonical event. Redis receives the same sanitized event for temporary delivery. SSE uses the decimal sequence as its `id`; reconnecting clients send `Last-Event-ID`, and NestJS requests events strictly after that cursor.

Compatibility is additive within version 1.0: consumers must ignore unknown payload fields but must reject unknown event types until the schema version is deliberately changed.
