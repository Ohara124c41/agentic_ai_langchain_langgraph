from __future__ import annotations

import re
from typing import Dict


NEGATIVE = {"angry", "upset", "bad", "terrible", "worst", "hate", "frustrated", "crash", "charged", "refund", "broken", "issue", "problem"}
POSITIVE = {"love", "great", "thanks", "awesome", "good", "works", "happy", "excellent", "appreciate"}


class SentimentAnalyzer:
    """Rule-based sentiment scorer in [-1, 1]."""

    def __init__(self, negative: set | None = None, positive: set | None = None):
        self.negative = negative or NEGATIVE
        self.positive = positive or POSITIVE

    def score(self, text: str) -> float:
        lowered = text.lower()
        neg_hits = sum(1 for w in self.negative if w in lowered)
        pos_hits = sum(1 for w in self.positive if w in lowered)
        total = neg_hits + pos_hits
        if total == 0:
            return 0.0
        raw = (pos_hits - neg_hits) / total
        # Soften extremes to avoid spurious -1
        return round(max(min(raw, 0.6), -0.6), 2)
