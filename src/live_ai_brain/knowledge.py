from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class KnowledgeChunk:
    source: str
    text: str


class KnowledgeBase:
    def __init__(self, chunks: list[KnowledgeChunk]) -> None:
        self.chunks = chunks

    @classmethod
    def from_product_dir(cls, product_dir: Path | str) -> "KnowledgeBase":
        root = Path(product_dir)
        chunks: list[KnowledgeChunk] = []
        for path in sorted(root.rglob("*")):
            if path.suffix.lower() not in {".md", ".txt"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore").strip()
            if text:
                chunks.append(KnowledgeChunk(source=str(path), text=text))
        return cls(chunks)

    def search(self, query: str, limit: int = 5) -> list[KnowledgeChunk]:
        terms = [term for term in query.strip().split() if term]
        scored: list[tuple[int, KnowledgeChunk]] = []
        for chunk in self.chunks:
            haystack = chunk.text.lower()
            score = sum(haystack.count(term.lower()) for term in terms)
            if score > 0:
                scored.append((score, chunk))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [chunk for _, chunk in scored[:limit]]
