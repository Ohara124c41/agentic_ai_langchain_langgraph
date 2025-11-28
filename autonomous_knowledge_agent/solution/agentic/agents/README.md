## Agents Overview

- **Classifier/Router** (`classifier.py`): Heuristic intent + sentiment scorer; sets route (tools vs knowledge vs escalation).
- **Knowledge Resolver** (`knowledge.py`): Embedding search over CultPass KB + long-term history; drafts cited answer with confidence.
- **Tooling Agent** (`tools_agent.py`): Calls FastMCP tools for account/billing/reservation flows; records tool calls.
- **Escalation/Comms** (`escalation.py`): Summarizes context and raises escalation packet when confidence is low or errors occur.
- **State helpers** (`state.py`): Shared schema + init/log helpers for the LangGraph workflow.

Graph wiring lives in `agentic/workflow.py`.
