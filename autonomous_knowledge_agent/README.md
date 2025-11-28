# Autonomous Knowledge Agent (LangGraph)

LangGraph-based multi-agent support workflow for UDA-Hub. It classifies tickets, retrieves knowledge, calls FastMCP tools backed by SQLite, applies sentiment/urgency signals, and escalates when confidence is low.

## What’s Included
- **Solution** (`solution/`): Complete implementation (agents, tools, workflow, notebooks, data).
- **Starter** (`starter/`): Original scaffold with TODOs (left for reference).
- **Requirements**: `requirements.txt` at repo root.

## Architecture (solution)
- Supervisor-led LangGraph with agents for classification/routing, RAG answer drafting, tool execution, and escalation.
- FastMCP-style tools: `account_lookup`, `plan_update_or_refund`, `log_ticket_note`, `summarize_ticket_history`.
- Sentiment-aware routing plus per-turn state reset and checkpointing.
- Embedding-style semantic search over 14 CultPass KB articles (+ long-term memories).

## Setup
1) Create a virtualenv and install deps:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2) (Optional) Add a `.env` in `solution/` with any API keys you use (not required for the heuristic embedder).

## Data/DB Seeding (solution/)
Run notebooks in order:
1) `01_external_db_setup.ipynb` → builds `data/external/cultpass.db` (users, subscriptions, experiences, reservations).
2) `02_core_db_setup.ipynb` → builds `data/core/udahub.db` and loads 14 KB articles.
If you see a file-lock `PermissionError`, close handles on the `.db` files or delete them before rerunning.

## Running the Agent
1) Open `03_agentic_app.ipynb`.
2) Import `from agentic.workflow import orchestrator`.
3) Run the REPL cell: `chat_interface(orchestrator, "ticket-1")`. It injects a default email so tools can run; provide another email in the ticket payload if desired.
4) Example prompts:
   - “How do I reserve an event?”
   - “I need a refund for my CultPass”
   - “My app crashes on iOS when opening reservations.”
   - “I need wheelchair access for tomorrow’s event.”

## Tests/Demos
Run lightweight checks after seeding DBs:
```bash
cd solution
python -m pytest
```

## File Map (key solution files)
- `agentic/workflow.py` — LangGraph wiring.
- `agentic/agents/` — classifier, knowledge resolver, tooling agent, escalation, state helpers.
- `agentic/tools/` — FastMCP registry, DB ops, sentiment, lightweight embedder.
- `data/external/cultpass_articles.jsonl` — expanded KB (14 articles).
- `tests/test_workflow.py` — sample assertions for RAG/tool paths.

## Notes
- Checkpointing uses `MemorySaver`; `init_node` resets per turn to avoid stale state while keeping thread_id compatibility.
