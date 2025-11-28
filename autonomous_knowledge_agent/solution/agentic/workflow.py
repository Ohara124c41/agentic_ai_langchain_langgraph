from __future__ import annotations

from typing import Dict
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from agentic.agents.state import WorkflowState, init_state, log
from agentic.agents.classifier import classifier_node
from agentic.agents.knowledge import knowledge_node
from agentic.agents.tools_agent import tool_node
from agentic.agents.escalation import escalation_node


def init_node(state: WorkflowState) -> WorkflowState:
    # Fresh state for each turn; only carry current messages/ticket to avoid stale escalations.
    base = init_state(ticket=state.get("ticket", {}), messages=state.get("messages", []))
    return log(base, "init: normalized state")


def route_after_classification(state: WorkflowState) -> str:
    classification = state.get("classification", {})
    intent = classification.get("intent", "unknown")
    # Billing/account go to tools; everything else try knowledge first.
    if intent in {"billing", "refund", "account"}:
        return "tools"
    return "knowledge"


def after_knowledge(state: WorkflowState) -> str:
    if state.get("answer"):
        return "finalize"
    return "escalate"


def after_tools(state: WorkflowState) -> str:
    if state.get("answer"):
        return "finalize"
    return "escalate"


def finalize_node(state: WorkflowState) -> WorkflowState:
    messages = state.get("messages", [])
    escalation = state.get("escalation") or {}
    # Avoid double-posting if the last message already matches the answer/escalation.
    if messages and isinstance(messages[-1], AIMessage):
        last = messages[-1].content
        if escalation.get("escalate") and "Escalated" in last:
            return log(state, "finalize: reuse existing escalation message")
        if not escalation.get("escalate") and state.get("answer") and last == state.get("answer"):
            return log(state, "finalize: reuse existing answer message")

    if isinstance(escalation, dict) and escalation.get("escalate"):
        content = f"Escalated: {escalation.get('summary','')}"
    else:
        content = state.get("answer") or "No response generated."
    messages.append(AIMessage(content=content))
    state["messages"] = messages
    return log(state, "finalize: responded")


graph = StateGraph(WorkflowState)

graph.add_node("init", init_node)
graph.add_node("classify", classifier_node)
graph.add_node("knowledge", knowledge_node)
graph.add_node("tools", tool_node)
graph.add_node("escalate", escalation_node)
graph.add_node("finalize", finalize_node)

graph.add_edge(START, "init")
graph.add_edge("init", "classify")
graph.add_conditional_edges("classify", route_after_classification, {"knowledge": "knowledge", "tools": "tools", "escalate": "escalate"})
graph.add_conditional_edges("knowledge", after_knowledge, {"finalize": "finalize", "escalate": "escalate"})
graph.add_conditional_edges("tools", after_tools, {"finalize": "finalize", "escalate": "escalate"})
graph.add_edge("escalate", "finalize")
graph.add_edge("finalize", END)

# Compile with MemorySaver; init_node resets per turn to avoid stale state.
orchestrator = graph.compile(checkpointer=MemorySaver())
