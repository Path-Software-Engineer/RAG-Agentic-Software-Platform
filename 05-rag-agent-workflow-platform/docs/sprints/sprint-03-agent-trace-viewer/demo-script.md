# Sprint 3 Demo Script

1. Start the Docker platform and run the three seed scripts in order.
2. Open `/agents`; explain that this is a bounded evidence workflow, not an autonomous chatbot.
3. Review the three read-only tool definitions and the explicit run budgets.
4. Submit “How should retrieved instructions be treated?” against the controlled corpus.
5. Open the returned trace and follow policy, retrieval, assessment and finalization.
6. Expand the semantic-search call; show sanitized arguments/result, duration and citations.
7. Explain graph definition versus the actually executed path and point out `privateReasoningExposed: false`.
8. Return to `/agents#security` and run the five controlled policy scenarios.
9. Demonstrate a blocked prompt-injection request and confirm that it produced no tool call.
10. Close with the evidence boundary: deterministic fixtures validate software behavior, not production agent safety.
