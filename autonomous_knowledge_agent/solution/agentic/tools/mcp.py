from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

from agentic.tools import ops


@dataclass
class FastMCPTool:
    name: str
    description: str
    func: Callable[..., Any]

    def __call__(self, **kwargs: Any) -> Any:
        return self.func(**kwargs)


class FastMCPRegistry:
    """Lightweight FastMCP-style registry to expose tools to agents."""

    def __init__(self):
        self.tools: Dict[str, FastMCPTool] = {}

    def register(self, tool: FastMCPTool) -> None:
        self.tools[tool.name] = tool

    def get(self, name: str) -> Optional[FastMCPTool]:
        return self.tools.get(name)

    def call(self, name: str, **kwargs: Any) -> Dict[str, Any]:
        tool = self.get(name)
        if not tool:
            return {"error": f"tool_not_found:{name}"}
        try:
            return {"result": tool(**kwargs), "tool": name}
        except Exception as e:
            return {"error": f"tool_error:{name}:{e}"}

    def list_tools(self) -> Dict[str, str]:
        return {name: t.description for name, t in self.tools.items()}


def default_registry() -> FastMCPRegistry:
    registry = FastMCPRegistry()
    registry.register(
        FastMCPTool(
            name="account_lookup",
            description="Lookup CultPass user/account/subscription/reservations by email.",
            func=lambda email, **_: ops.account_lookup(email=email),
        )
    )
    registry.register(
        FastMCPTool(
            name="plan_update_or_refund",
            description="Simulate plan downgrade/credit/refund decision with approval flag.",
            func=lambda email, action="credit", reason="", **_: ops.plan_update_or_refund(
                email=email, action=action, reason=reason
            ),
        )
    )
    registry.register(
        FastMCPTool(
            name="log_ticket_note",
            description="Log a note to the Udahub ticket history.",
            func=lambda ticket_id, content, **_: ops.log_ticket_note(ticket_id=ticket_id, content=content),
        )
    )
    registry.register(
        FastMCPTool(
            name="summarize_ticket_history",
            description="Summarize recent ticket messages for a given user_id.",
            func=lambda user_id, **_: ops.summarize_ticket_history(user_id=user_id),
        )
    )
    return registry
