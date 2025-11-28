## UDA-Hub Agentic Design

### Architecture Pattern
Supervisor-led, hierarchical routing with specialized agents:
- **Supervisor**: Entry point, orchestrates graph, aggregates signals (classification, sentiment, memory) and decides next step.
- **Classifier/Router**: Labels ticket (intent, urgency, channel) + sentiment; proposes route and confidence.
- **Knowledge Resolver**: Runs embedding RAG over CultPass KB (14+ articles) + prior tickets, drafts answer, scores confidence.
- **Tooling Agent**: Executes FastMCP-exposed ops (account lookup, subscription update/refund simulation, ticket note logging).
- **Escalation/Comms Agent**: Summarizes context for human handoff or final customer response when confidence low.
- **Memory Service**: Short-term via LangGraph checkpoint (thread_id); long-term via vector store of past resolutions/preferences.


### Key Decisions
- **Embeddings/RAG**: Use `text-embedding-3-small` (or local fallback) via `langchain_openai` to index KB articles; semantic search with top-k + rerank; include metadata for source tagging.
- **Sentiment**: Lightweight sentiment scorer (rule-based polarity) to raise priority and lower confidence thresholds.
- **FastMCP**: Tools exposed through a FastMCP server wrapper: `account_lookup`, `plan_update_or_refund` (sim), `log_ticket_note`, optionally `knowledge_search`; structured outputs and validation.
- **Routing Logic**: Supervisor chooses branch based on classifier label + confidence + sentiment + presence of KB hits/tools; at least one routing decision derived from classification.
- **Memory**:
  - Short-term: LangGraph `MemorySaver` keyed by `thread_id`.
  - Long-term: Vector store over past `TicketMessage` and resolutions; retrieved in Knowledge Resolver to personalize answers.
- **Escalation**: Trigger when RAG/tool confidence < threshold or high negative sentiment; produce concise summary + next step tags.

### Agents & Responsibilities
- **Classifier/Router**: Detect intent (billing, account, access, reservation, content, bug, refund, unknown), urgency, sentiment. Emits route suggestion + confidence.
- **Knowledge Resolver**: Embedding search, build cited answer, compute confidence; uses long-term memory; yields draft + score.
- **Tooling Agent**: Calls FastMCP tools; validates inputs; returns structured results for billing/account actions.
- **Escalation/Comms**: Summarize conversation, risks, attempted tools, and propose human follow-up.
- **Supervisor**: Central state mutation, decides next edge, composes final response or escalation packet.

### Inputs/Outputs
- **Input**: Ticket text, metadata (channel, urgency, ticket_id/thread_id, customer_id/email, tags), history (messages), sentiment score.
- **Output**: Resolution message or escalation bundle (summary, steps taken, suggested next action), plus logs of tools and routes.

### State Schema (graph)
- `messages`: list of LangChain messages
- `ticket`: dict with id/user/channel/urgency/tags
- `classification`: labels + confidence + sentiment
- `knowledge_hits`: retrieved docs + scores
- `tool_calls`: records of FastMCP tool invocations/results
- `answer`: final text
- `escalation`: boolean + summary + reason

### Testing Strategy
- Synthetic tickets per rubric (billing refund, account access, reservation, technical issue, unknown → escalate).
- Validate routing choice vs expected label.
- Ensure RAG returns citations for KB-backed questions.
- Ensure tool path fires for billing/account intents.
- Ensure escalation triggers for low-confidence or negative sentiment.
