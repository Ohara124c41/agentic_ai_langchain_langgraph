from __future__ import annotations

from typing import List
from langchain_core.messages import AIMessage

from agentic.agents.state import WorkflowState, log
from agentic.tools.knowledge_base import KnowledgeBase
from agentic.tools import ops


def build_answer(hits: List[dict], query: str) -> str:
    lines = ["Here is what I found:", ""]
    for idx, h in enumerate(hits, start=1):
        lines.append(f"{idx}. {h['title']} (source: {h['source']}, score={h['score']})")
    lines.append("")
    best = hits[0]
    lines.append(f"Suggested resolution: {best['content']}")
    return "\n".join(lines)


def knowledge_node(state: WorkflowState) -> WorkflowState:
    messages = state.get("messages", [])
    query = messages[-1].content if messages else ""
    kb = KnowledgeBase()
    kb.load_jsonl("data/external/cultpass_articles.jsonl", account_id="cultpass")

    ticket = state.get("ticket", {})
    user_id = ticket.get("user_id") or ""
    if user_id:
        history = ops.summarize_ticket_history(user_id=user_id)
        if history:
            kb.add_memory(history, {"id": f"hist-{user_id}", "title": "recent_history", "source": "udahub"})

    hits = kb.search(query, k=4)
    state["knowledge_hits"] = hits
    if not hits:
        state["answer"] = None
        state["escalation"] = {"escalate": True, "reason": "no_hits", "summary": "No KB hit", "priority": "normal"}
        state["messages"] = messages + [AIMessage(content="I could not find a relevant article; escalating.")]
        return log(state, "knowledge: no hits, escalate")

    confidence = hits[0]["score"]
    answer = build_answer(hits, query)
    state["answer"] = answer
    state["escalation"] = {"escalate": False}
    state["messages"] = messages + [AIMessage(content=answer)]
    state["classification"]["confidence"] = max(state["classification"].get("confidence", 0.0), round(confidence, 2))
    return log(state, f"knowledge: {len(hits)} hits, top={confidence:.2f}")
