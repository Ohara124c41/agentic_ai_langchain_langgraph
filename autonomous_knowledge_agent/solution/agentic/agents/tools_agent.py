from __future__ import annotations

from langchain_core.messages import AIMessage

from agentic.agents.state import WorkflowState, log
from agentic.tools.mcp import default_registry


registry = default_registry()


def _choose_tool(intent: str) -> str | None:
    if intent in {"billing", "refund"}:
        return "plan_update_or_refund"
    if intent in {"account", "reservation"}:
        return "account_lookup"
    return None


def _format_tool_result(name: str, result: dict) -> str:
    if name == "account_lookup" and isinstance(result, dict):
        user = result.get("user", {})
        sub = result.get("subscription", {})
        reservations = result.get("reservations", [])
        lines = [
            f"Account: {user.get('name','n/a')} ({user.get('email','n/a')})",
            f"Status: {sub.get('status','n/a')} | Tier: {sub.get('tier','n/a')} | Quota: {sub.get('monthly_quota','n/a')}",
        ]
        if reservations:
            lines.append("Reservations:")
            for r in reservations:
                lines.append(f"- {r.get('experience_id')} [{r.get('status')}] (resv {r.get('reservation_id')})")
        else:
            lines.append("Reservations: none on file.")
        return "\n".join(lines)
    if name == "plan_update_or_refund" and isinstance(result, dict):
        return f"Action: {result.get('action')} | Approved: {result.get('approved')} | Note: {result.get('note')}"
    return str(result)


def tool_node(state: WorkflowState) -> WorkflowState:
    messages = state.get("messages", [])
    classification = state.get("classification", {})
    intent = classification.get("intent", "unknown")
    ticket = state.get("ticket", {})
    email = ticket.get("email") or ticket.get("user_email") or ""
    tool_name = _choose_tool(intent)

    if not tool_name:
        # If no tool but we have KB hits/answer, do not escalate here; fallback handled elsewhere.
        state["escalation"] = {"escalate": False}
        state["messages"] = messages + [AIMessage(content="No applicable tool; continuing without tool.")]
        return log(state, "tools: no tool for intent")

    if tool_name in {"plan_update_or_refund", "account_lookup"} and not email:
        state["escalation"] = {"escalate": True, "reason": "missing_email", "summary": "Email required for tool", "priority": "normal"}
        state["messages"] = messages + [AIMessage(content="Need an email to proceed; escalating.")]
        return log(state, "tools: missing email")

    payload = {"email": email}
    if tool_name == "plan_update_or_refund":
        payload["action"] = "credit" if intent == "billing" else "downgrade"
        payload["reason"] = classification.get("rationale", "")

    result = registry.call(tool_name, **payload)
    success = "error" not in result
    tool_record = {
        "name": tool_name,
        "input": payload,
        "output": result,
        "success": success,
        "error": result.get("error") if not success else None,
    }
    calls = state.get("tool_calls", [])
    calls.append(tool_record)
    state["tool_calls"] = calls

    if success:
        formatted = _format_tool_result(tool_name, result.get("result"))
        content = f"Tool `{tool_name}` result:\n{formatted}"
        state["answer"] = content
        state["classification"]["confidence"] = max(state["classification"].get("confidence", 0.0), 0.7)
        state["messages"] = messages + [AIMessage(content=content)]
        return log(state, f"tools: {tool_name} success")

    state["answer"] = None
    state["messages"] = messages + [AIMessage(content="Tool failed; escalating to human support.")]
    return log(state, f"tools: {tool_name} failed: {result.get('error')}")
