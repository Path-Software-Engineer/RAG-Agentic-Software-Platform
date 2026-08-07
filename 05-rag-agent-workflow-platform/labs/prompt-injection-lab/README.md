# Prompt Injection Lab

Purpose: regression-test the versioned request policy and retrieved-content trust boundary without attacking an external service.

The lab uses the controlled scenarios in `packages/contracts/fixtures/security-scenarios.json` and the Python policy tests. Inputs are synthetic. Only scenario category, expected/observed disposition and policy code belong in reports; secrets, harmful payload variants and chain-of-thought do not.

Run through the complete gate or execute:

```powershell
$env:PYTHONPATH = (Resolve-Path "ai-services\rag-agent-service").Path
python -m pytest ai-services\rag-agent-service\tests\test_agent_workflow.py -q
```

Passing this lab validates the current fixture-policy contract only.
