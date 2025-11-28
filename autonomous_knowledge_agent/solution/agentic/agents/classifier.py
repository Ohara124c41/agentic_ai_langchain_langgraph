from __future__ import annotations

import re
from typing import Dict, List
from langchain_core.messages import BaseMessage

from agentic.agents.state import WorkflowState, log
from agentic.tools.sentiment import SentimentAnalyzer


INTENT_KEYWORDS: Dict[str, List[str]] = {
    "billing": ["charge", "billing", "refund", "payment", "credit", "card", "invoice"],
    "account": ["account", "profile", "login", "sign in", "2fa", "password", "access"],
    "reservation": ["reserve", "booking", "event", "slot", "schedule", "reschedule", "cancel reservation"],
    "technical": ["crash", "bug", "error", "slow", "performance", "app"],
    "content": ["article", "information", "what is included", "benefit", "subscription"],
    "unknown": [],
}


def classify_intent(text: str) -> str:
    lowered = text.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(k in lowered for k in keywords):
            return intent
    return "unknown"


def classifier_node(state: WorkflowState) -> WorkflowState:
    """Heuristic classifier + sentiment scorer. Returns updated state with classification."""
    messages: List[BaseMessage] = state.get("messages", [])
    ticket = state.get("ticket", {})
    latest = messages[-1].content if messages else ""

    sentiment = SentimentAnalyzer().score(latest)
    intent = classify_intent(latest)
    urgency = ticket.get("urgency") or ("high" if sentiment < -0.4 else "normal")

    confidence = 0.6 if intent != "unknown" else 0.35
    if abs(sentiment) > 0.6:
        confidence += 0.05
    rationale = f"intent={intent}, sentiment={sentiment:.2f}, urgency={urgency}"

    state["classification"] = {
        "intent": intent,
        "confidence": round(confidence, 2),
        "sentiment": round(sentiment, 2),
        "urgency": urgency,
        "route": intent,
        "rationale": rationale,
    }
    return log(state, f"classifier: {rationale}")
