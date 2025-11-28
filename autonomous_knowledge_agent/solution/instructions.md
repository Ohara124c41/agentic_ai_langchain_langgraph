# UDA-Hub Working Notes

Tracking rubric items, tasks, and decisions so context isn’t lost.

## Required Deliverables
- Design docs/diagram in `agentic/design` describing the multi-agent architecture (Supervisor, Classifier/Router, Resolver, Escalation, Memory/KG specialist, Tool caller).
- Implement agents/tools/workflow in code (no prebuilt graph) under `agentic/agents`, `agentic/tools`, `agentic/workflow.py`.
- Expand knowledge base: grow `cultpass_articles.jsonl` from 4 to ≥14 diverse articles; run data notebooks to seed DBs.
- Implement embeddings-backed retrieval + sentiment analysis + FastMCP tooling; integrate in workflow.
- Provide tests/demo flows to show end-to-end ticket processing (classification → routing → retrieval/tools → resolve/escalate) with logging.
- Keep notebooks’ non-TODO cells untouched; do not delete/merge cells.

## Rubric Checklist
1. **Data/KB**: DB tables created; knowledge base has ≥10 new diverse articles; retrieval demo works.
2. **Architecture**: Documented design + diagram; ≥4 specialized agents; roles/responsibilities defined; info flow explained.
3. **Implementation**: LangGraph matches design; routing based on classification/metadata; state/message passing correct.
4. **Knowledge & Tools**: Embedding/RAG retrieval with confidence + escalation path; ≥2 DB-backed tools (account lookup, subscription/refund, etc.) with error handling; integrated via FastMCP interface.
5. **Memory**: Short-term (session/thread) + long-term (interaction history/preferences) persisted; used in decisions.
6. **Integration/Testing**: End-to-end run covering success + escalation; structured logging of routing, tools, outcomes; sample tests/cases included.
7. **Extras requested**: Sentiment analysis, FastMCP tooling, embeddings search. (A/B not required.)

## Implementation Plan (high level)
- Data: Add 10+ articles; ensure notebooks consume updated JSONL.
- Design: Write architecture README + Mermaid/ASCII diagram; describe agent roles/flows, memory, sentiment, RAG, FastMCP tools.
- Tools: Build DB abstraction helpers (ORM/session), knowledge search (embeddings), sentiment scorer, MCP-exposed support ops (account lookup, refund/plan change, ticket note logging).
- Agents: Classifier/Router, Knowledge Resolver, Tool Ops, Escalation/Comms; Supervisor coordinates; sentiment influences escalation/priority.
- Workflow: Custom LangGraph (no prebuilt) with state schema, checkpoints, routing edges; integrate memory stores.
- Tests/demo: Add sample tickets/test harness to validate routing, retrieval, tool calls, escalation.
