import hashlib
import math
import re
from dataclasses import dataclass
from pathlib import Path


TOKEN = re.compile(r"[a-z0-9-]+", re.I)


@dataclass
class Chunk:
    source: str
    text: str
    vector: list[float]


def embed(text: str, dimensions: int = 256) -> list[float]:
    vector = [0.0] * dimensions
    for token in TOKEN.findall(text.lower()):
        digest = hashlib.sha256(token.encode()).digest()
        index = int.from_bytes(digest[:2], "big") % dimensions
        vector[index] += 1 if digest[2] % 2 else -1
    norm = math.sqrt(sum(value * value for value in vector)) or 1
    return [value / norm for value in vector]


def cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


class KnowledgeBase:
    def __init__(self, root: str = "knowledge"):
        self.root = Path(root)
        self.chunks: list[Chunk] = []
        self.reload()

    def reload(self) -> int:
        self.chunks = []
        if not self.root.exists():
            return 0
        for path in self.root.glob("*.md"):
            paragraphs = [p.strip() for p in path.read_text(encoding="utf-8").split("\n\n") if p.strip()]
            for paragraph in paragraphs:
                self.chunks.append(Chunk(path.name, paragraph, embed(paragraph)))
        return len(self.chunks)

    def search(self, query: str, limit: int = 3) -> list[tuple[Chunk, float]]:
        query_vector = embed(query)
        terms = set(TOKEN.findall(query.lower()))
        scored = []
        for chunk in self.chunks:
            lexical = len(terms & set(TOKEN.findall(chunk.text.lower()))) / max(len(terms), 1)
            score = 0.65 * max(cosine(query_vector, chunk.vector), 0) + 0.35 * lexical
            scored.append((chunk, round(score, 3)))
        return sorted(scored, key=lambda item: item[1], reverse=True)[:limit]
