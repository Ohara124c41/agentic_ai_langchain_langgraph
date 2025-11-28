from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in text.split()]


class SimpleEmbedder:
    """Lightweight, dependency-free embedding approximator using bag-of-words norms."""

    def embed(self, text: str) -> Dict[str, float]:
        tokens = _tokenize(text)
        vec: Dict[str, float] = {}
        for t in tokens:
            vec[t] = vec.get(t, 0.0) + 1.0
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        return {k: v / norm for k, v in vec.items()}

    def similarity(self, a: Dict[str, float], b: Dict[str, float]) -> float:
        # cosine on sparse dicts
        if not a or not b:
            return 0.0
        score = 0.0
        for k, v in a.items():
            score += v * b.get(k, 0.0)
        return score


@dataclass
class KBEntry:
    article_id: str
    title: str
    content: str
    tags: List[str]
    embedding: Dict[str, float]
    source: str


class KnowledgeBase:
    """Minimal semantic search over CultPass articles and long-term memories."""

    def __init__(self, embedder: SimpleEmbedder | None = None):
        self.embedder = embedder or SimpleEmbedder()
        self.entries: List[KBEntry] = []

    def load_jsonl(self, path: str | Path, account_id: str = "cultpass") -> None:
        path = Path(path)
        raw = path.read_text(encoding="utf-8").splitlines()
        for idx, line in enumerate(raw):
            data = json.loads(line)
            article_id = f"{account_id}-{idx+1}"
            tags = (
                data.get("tags", "")
                .replace(" ", "")
                .split(",")
                if isinstance(data.get("tags"), str)
                else data.get("tags", [])
            )
            embedding = self.embedder.embed(f"{data.get('title','')} {data.get('content','')}")
            self.entries.append(
                KBEntry(
                    article_id=article_id,
                    title=data.get("title", ""),
                    content=data.get("content", ""),
                    tags=tags,
                    embedding=embedding,
                    source=str(path),
                )
            )

    def add_memory(self, text: str, meta: Dict[str, str]) -> None:
        embedding = self.embedder.embed(text)
        entry = KBEntry(
            article_id=meta.get("id", f"mem-{len(self.entries)+1}"),
            title=meta.get("title", "memory"),
            content=text,
            tags=meta.get("tags", "").split(",") if meta.get("tags") else [],
            embedding=embedding,
            source=meta.get("source", "memory"),
        )
        self.entries.append(entry)

    def search(self, query: str, k: int = 3) -> List[Dict]:
        q_embed = self.embedder.embed(query)
        scored: List[Tuple[float, KBEntry]] = []
        for entry in self.entries:
            sim = self.embedder.similarity(q_embed, entry.embedding)
            if sim > 0:
                scored.append((sim, entry))
        scored.sort(key=lambda x: x[0], reverse=True)
        hits = []
        for score, entry in scored[:k]:
            hits.append(
                {
                    "article_id": entry.article_id,
                    "title": entry.title,
                    "content": entry.content,
                    "tags": entry.tags,
                    "score": round(score, 3),
                    "source": entry.source,
                }
            )
        return hits
