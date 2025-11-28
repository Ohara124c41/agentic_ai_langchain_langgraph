from __future__ import annotations

from langchain_core.messages import AIMessage

from agentic.agents.state import WorkflowState, log


def escalation_node(state: WorkflowState) -> WorkflowState:
    classification = state.get("classification", {})
    intent = classification.get("intent", "unknown")
    sentiment = classification.get("sentiment", 0.0)
    knowledge_hits = state.get("knowledge_hits", [])
    tool_calls = state.get("tool_calls", [])

    summary_lines = [
        f"Intent: {intent}",
        f"Sentiment: {sentiment}",
        f"Knowledge hits: {len(knowledge_hits)}",
        f"Tools attempted: {len(tool_calls)}",
    ]
    if knowledge_hits:
        summary_lines.append(f"Top hit: {knowledge_hits[0].get('title')}")
    if tool_calls:
        summary_lines.append(f"Last tool: {tool_calls[-1].get('name')} -> {tool_calls[-1].get('output')}")

    summary = "\n".join(summary_lines)
    state["escalation"] = {
        "escalate": True,
        "reason": "low_confidence_or_error",
        "summary": summary,
        "priority": "high" if sentiment < -0.3 else "normal",
    }
    messages = state.get("messages", [])
    state["messages"] = messages + [AIMessage(content=f"Escalating to human support.\n{summary}")]
    return log(state, "escalation: raised")
