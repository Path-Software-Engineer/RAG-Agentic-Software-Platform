from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

RunStatus = Literal["queued", "running", "waiting", "completed", "failed", "cancelled", "blocked"]
RunOutcome = Literal[
    "answered",
    "insufficient_evidence",
    "policy_blocked",
    "budget_exhausted",
    "cancelled",
    "failed",
]
TraceEventType = Literal[
    "run_started",
    "step_started",
    "step_completed",
    "step_failed",
    "tool_called",
    "tool_completed",
    "tool_failed",
    "policy_blocked",
    "run_completed",
    "run_failed",
    "run_cancelled",
]
AgentToolName = Literal["semantic_search", "document_lookup", "evaluation_lookup"]


def default_agent_tools() -> list[AgentToolName]:
    return ["semantic_search"]


class AgentBudget(BaseModel):
    max_steps: int = Field(default=8, ge=4, le=16)
    max_tool_calls: int = Field(default=3, ge=1, le=6)
    overall_timeout_ms: int = Field(default=8_000, ge=500, le=20_000)
    per_tool_timeout_ms: int = Field(default=3_000, ge=250, le=8_000)


class AgentUsage(BaseModel):
    steps: int = Field(default=0, ge=0)
    tool_calls: int = Field(default=0, ge=0)
    elapsed_ms: float = Field(default=0, ge=0)


class AgentRunRequest(BaseModel):
    goal: str = Field(min_length=3, max_length=500)
    workflow_id: Literal["bounded-research-v1"] = "bounded-research-v1"
    document_version_ids: list[UUID] = Field(default_factory=list, max_length=50)
    allowed_tool_names: list[AgentToolName] = Field(default_factory=default_agent_tools)
    budget: AgentBudget = Field(default_factory=AgentBudget)
    idempotency_key: str = Field(min_length=8, max_length=120, pattern=r"^[A-Za-z0-9._:-]+$")
    correlation_id: UUID

    @field_validator("goal")
    @classmethod
    def normalize_goal(cls, value: str) -> str:
        normalized = " ".join(value.split())
        if len(normalized) < 3:
            raise ValueError("goal must contain visible text")
        return normalized

    @field_validator("allowed_tool_names")
    @classmethod
    def unique_tools(cls, value: list[AgentToolName]) -> list[AgentToolName]:
        if not value:
            raise ValueError("at least one allowlisted tool is required")
        if len(set(value)) != len(value):
            raise ValueError("allowed_tool_names must be unique")
        return value


class AgentCitation(BaseModel):
    citation_id: UUID
    document_id: UUID
    document_version_id: UUID
    chunk_id: UUID
    rank: int = Field(ge=1)
    score: float = Field(ge=-1, le=1)
    snippet: str = Field(max_length=360)


class AgentStepResource(BaseModel):
    step_id: UUID
    node_id: str
    sequence_number: int = Field(ge=1)
    status: Literal["running", "completed", "failed", "blocked", "cancelled"]
    started_at: datetime
    completed_at: datetime | None = None
    duration_ms: float | None = Field(default=None, ge=0)
    error_code: str | None = None


class AgentToolCallResource(BaseModel):
    tool_call_id: UUID
    step_id: UUID
    tool_name: str
    status: Literal["running", "completed", "failed", "blocked"]
    sanitized_arguments: dict[str, Any]
    sanitized_result: dict[str, Any] | None = None
    started_at: datetime
    completed_at: datetime | None = None
    duration_ms: float | None = Field(default=None, ge=0)
    error_code: str | None = None


class AgentTraceEvent(BaseModel):
    event_id: UUID
    run_id: UUID
    sequence_number: int = Field(ge=1)
    event_type: TraceEventType
    node_id: str | None = None
    payload: dict[str, Any]
    timestamp: datetime


class AgentRunResource(BaseModel):
    run_id: UUID
    thread_id: UUID
    workflow_id: str
    status: RunStatus
    outcome: RunOutcome | None = None
    goal: str
    answer: str | None = None
    allowed_tool_names: list[str]
    document_version_ids: list[UUID]
    budget: AgentBudget
    usage: AgentUsage
    citations: list[AgentCitation] = Field(default_factory=list)
    idempotency_key: str
    correlation_id: UUID
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_code: str | None = None


class AgentRunSummary(BaseModel):
    run_id: UUID
    workflow_id: str
    status: RunStatus
    outcome: RunOutcome | None = None
    goal: str
    citation_count: int = Field(ge=0)
    created_at: datetime
    completed_at: datetime | None = None


class AgentGraphNode(BaseModel):
    node_id: str
    label: str
    kind: Literal["policy", "tool", "decision", "terminal"]


class AgentGraphEdge(BaseModel):
    source: str
    target: str
    condition: str


class AgentTraceResource(BaseModel):
    run: AgentRunResource
    nodes: list[AgentGraphNode]
    edges: list[AgentGraphEdge]
    steps: list[AgentStepResource]
    tool_calls: list[AgentToolCallResource]
    events: list[AgentTraceEvent]
    private_reasoning_exposed: Literal[False] = False


class ToolDefinition(BaseModel):
    name: str
    description: str
    permission: Literal["documents:read", "evaluations:read"]
    input_schema: dict[str, Any]
    timeout_ms: int = Field(ge=250, le=8_000)
    max_result_bytes: int = Field(ge=256, le=32_768)
    read_only: Literal[True] = True


class SecurityScenarioResult(BaseModel):
    scenario_id: str
    category: Literal[
        "benign", "prompt_injection", "tool_abuse", "data_exfiltration", "denial_of_wallet"
    ]
    expected: Literal["allowed", "blocked"]
    observed: Literal["allowed", "blocked", "failed"]
    passed: bool
    policy_code: str | None = None


class SecurityEvaluationResource(BaseModel):
    evaluation_id: UUID
    policy_version: str
    scenario_count: int = Field(ge=1)
    passed_count: int = Field(ge=0)
    blocked_count: int = Field(ge=0)
    failed_count: int = Field(ge=0)
    passed: bool
    scenarios: list[SecurityScenarioResult]
    created_at: datetime
