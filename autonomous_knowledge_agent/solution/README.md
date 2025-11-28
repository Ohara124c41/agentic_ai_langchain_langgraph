# UDA-Hub Solution

- Multi-agent LangGraph workflow in `agentic/workflow.py` (Supervisor-led with classifier, knowledge resolver, tooling agent, escalation).
- Agents/tools live under `agentic/agents` and `agentic/tools` (FastMCP registry, sentiment, embeddings, DB ops).
- Knowledge base expanded to 14 articles in `data/external/cultpass_articles.jsonl`.
- Data setup: run `01_external_db_setup.ipynb` then `02_core_db_setup.ipynb` (modify only TODO cells).
- Demo: run `03_agentic_app.ipynb` (imports `orchestrator`) or call `chat_interface(orchestrator, ticket_id)` from `utils.py`.

See `instructions.md` for full rubric checklist and implementation notes.
