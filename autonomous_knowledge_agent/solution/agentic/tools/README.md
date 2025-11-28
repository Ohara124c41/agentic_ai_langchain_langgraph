## Tools Overview

- `knowledge_base.py`: Dependency-light embedding search over CultPass KB + long-term memories.
- `sentiment.py`: Rule-based sentiment scorer ([-1, 1]).
- `db.py`: Safe session context for SQLite.
- `ops.py`: Database-backed operations (account lookup, refund/plan credit simulation, ticket note logging, ticket history summary).
- `mcp.py`: FastMCP-style registry exposing tools to agents.

These are wired into the workflow via `tools_agent.py` and FastMCP registry.
