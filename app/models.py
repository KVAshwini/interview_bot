from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AnswerMatch:
    id: str
    category: str
    topic: str
    question: str
    score: float
    instant_answer: str
    detailed_answer: str
    keywords: list[str]
    source_file: str
    raw: dict[str, Any]

    @property
    def confidence(self) -> str:
        if self.score >= 0.85:
            return "high"
        if self.score >= 0.60:
            return "medium"
        return "low"
