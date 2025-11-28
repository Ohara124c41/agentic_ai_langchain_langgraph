from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage


class TicketPayload(TypedDict, total=False):
    ticket_id: str
    user_id: str
    account_id: str
    channel: str
    urgency: str
    tags: List[str]
    metadata: Dict[str, Any]


class ClassificationResult(TypedDict, total=False):
    intent: str
    confidence: float
    sentiment: float
    urgency: str
    route: str
    rationale: str


class KnowledgeHit(TypedDict, total=False):
    title: str
    content: str
    score: float
    source: str
    tags: List[str]


class ToolCallRecord(TypedDict, total=False):
    name: str
    input: Dict[str, Any]
    output: Any
    success: bool
    error: Optional[str]


class EscalationPacket(TypedDict, total=False):
    escalate: bool
    reason: str
    summary: str
    priority: str


@dataclass
class AgentState:
    """Shared state for the LangGraph workflow."""

    messages: List[BaseMessage] = field(default_factory=list)
    ticket: TicketPayload = field(default_factory=dict)
    classification: ClassificationResult = field(default_factory=dict)
    knowledge_hits: List[KnowledgeHit] = field(default_factory=list)
    tool_calls: List[ToolCallRecord] = field(default_factory=list)
    answer: Optional[str] = None
    escalation: Optional[EscalationPacket] = None
    trace: List[str] = field(default_factory=list)

    def log(self, text: str) -> None:
        self.trace.append(text)


class WorkflowState(TypedDict, total=False):
    messages: List[BaseMessage]
    ticket: TicketPayload
    classification: ClassificationResult
    knowledge_hits: List[KnowledgeHit]
    tool_calls: List[ToolCallRecord]
    answer: Optional[str]
    escalation: Optional[EscalationPacket]
    trace: List[str]


def init_state(ticket: Optional[TicketPayload] = None, messages: Optional[List[BaseMessage]] = None) -> WorkflowState:
    """Helper to initialize a workflow state dictionary."""
    return WorkflowState(
        messages=messages or [],
        ticket=ticket or {},
        classification=ClassificationResult(),
        knowledge_hits=[],
        tool_calls=[],
        answer=None,
        escalation=None,
        trace=[],
    )


def log(state: WorkflowState, text: str) -> WorkflowState:
    trace = state.get("trace") or []
    trace.append(text)
    state["trace"] = trace
    return state
