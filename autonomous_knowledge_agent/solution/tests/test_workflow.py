from langchain_core.messages import HumanMessage

from agentic.workflow import orchestrator


def run_case(question: str, ticket_id: str = "demo", email: str | None = None):
    ticket = {"ticket_id": ticket_id}
    if email:
        ticket["email"] = email
    result = orchestrator.invoke(
        {"messages": [HumanMessage(content=question)], "ticket": ticket},
        config={"configurable": {"thread_id": ticket_id}},
    )
    return result["messages"][-1].content


def test_reservation_rag():
    answer = run_case("How do I reschedule my reservation?", "t1")
    assert "reschedule" in answer.lower() or "reservation" in answer.lower()


def test_billing_tool_fallback():
    answer = run_case("I need a refund for my CultPass", "t2", email="alice.kingsley@wonderland.com")
    assert "refund" in answer.lower() or "credit" in answer.lower()
