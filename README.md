# Agentic AI Projects (LangChain + LangGraph)

Three applied agentic builds:
- **EcoHome Energy Advisor** (`energy_advisor/`): RAG + tools for smart-home energy optimization.
- **DocDacity Document Assistant** (`report-building_agent/`): Intent-routed doc QA/summarization/calculation.
- **UDA-Hub Support Agent** (`autonomous_knowledge_agent/`): Multi-agent ticket triage with tools + sentiment + memory.

## Repo Layout
- `energy_advisor/` — EcoHome Energy Advisor (notebooks + agent/tools code).
- `report-building_agent/` — DocDacity assistant (CLI, routing, tools, diagrams).
- `autonomous_knowledge_agent/` — UDA-Hub multi-agent support system (solution + starter).
- `.gitignore`, `requirements.txt` per project.

## Quick Start (per project)
1) `cd <project>`
2) `python -m venv .venv && .venv\Scripts\activate`
3) `pip install -r requirements.txt`
4) Add any needed `.env` with API keys (see each project README).
5) Follow the project README for runs/tests (notebooks or CLI).

## Highlights
- **Energy Advisor**: DB + RAG setup notebooks, tool-backed agent with evaluation notebook and 10 test cases.
- **DocDacity**: Intent classification to QA/summarization/calculation agents, calculator tool, document search/read/stats, session memory and logging.
- **UDA-Hub**: LangGraph multi-agent (classifier, knowledge resolver, tooling, escalation), FastMCP tools over SQLite, sentiment-aware routing, KB with 14 articles, REPL demo, and tests.

## Run Entrypoints
- Energy: notebooks under `energy_advisor/ecohome_starter/` (run 01/02/03 in order).
- DocDacity: `cd report-building_agent/starter && python main.py`.
- UDA-Hub: `cd autonomous_knowledge_agent/solution && jupyter nbopen 03_agentic_app.ipynb` (or import `agentic.workflow.orchestrator` and use `chat_interface`).

## Notes
- Keep non-TODO notebook cells unchanged when working in starter folders.
- If SQLite files lock, close handles or delete the `.db` and rerun setup notebooks.
- No emojis/non-ASCII in code/logs.
