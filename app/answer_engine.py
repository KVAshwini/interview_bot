import json
import sqlite3

from app.config import DB_PATH
from app.db import all_items, connect
from app.memory import relevant_memory
from app.models import AnswerMatch
from app.speech_style import adapt_answer, quick_versions
from app.text_utils import similarity


def _row_to_match(row: sqlite3.Row, score: float) -> AnswerMatch:
    return AnswerMatch(
        id=row["id"],
        category=row["category"],
        topic=row["topic"],
        question=row["question"],
        score=score,
        instant_answer=row["instant_answer"],
        detailed_answer=row["detailed_answer"],
        keywords=json.loads(row["keywords"]),
        source_file=row["source_file"],
        raw=json.loads(row["raw_json"]),
    )


def _candidate_texts(row: sqlite3.Row) -> list[str]:
    alternates = json.loads(row["alternate_questions"])
    keywords = json.loads(row["keywords"])
    return [
        row["question"],
        *alternates,
        row["topic"],
        " ".join(keywords),
        row["searchable_text"],
    ]


def _best_score(query: str, row: sqlite3.Row) -> float:
    scores = [similarity(query, candidate) for candidate in _candidate_texts(row)]
    return max(scores) if scores else 0.0


def find_best_matches(query: str, limit: int = 3) -> list[AnswerMatch]:
    with connect(DB_PATH) as conn:
        scored = [
            _row_to_match(row, _best_score(query, row))
            for row in all_items(conn)
        ]
    return sorted(scored, key=lambda match: match.score, reverse=True)[:limit]


def format_match(match: AnswerMatch, mode: str = "instant", voice: str = "natural") -> str:
    keywords = ", ".join(match.keywords[:8])
    answer = match.instant_answer if mode == "instant" else match.detailed_answer
    natural = adapt_answer(answer) if voice == "natural" else answer
    memory_bits = relevant_memory(match.question)
    memory_text = ""
    if memory_bits:
        memory_text = "\n\nRelevant memory:\n" + "\n".join(
            f"- {item['name']} ({item['path']}, score {item['score']:.2f})"
            for item in memory_bits
        )
    return (
        f"[{match.confidence} confidence | score {match.score:.2f}]\n"
        f"Topic: {match.topic}\n"
        f"Matched: {match.question}\n\n"
        f"Natural read-aloud version:\n{natural}\n\n"
        f"Stored answer:\n{answer}\n\n"
        f"Keywords: {keywords}\n"
        f"Source: {match.source_file}"
        f"{memory_text}"
    )


def answer_payload(query: str, mode: str = "instant", limit: int = 3, voice: str = "natural") -> dict:
    matches = find_best_matches(query, limit=limit)
    return {
        "query": query,
        "mode": mode,
        "voice": voice,
        "matches": [
            {
                "id": match.id,
                "category": match.category,
                "topic": match.topic,
                "question": match.question,
                "score": match.score,
                "confidence": match.confidence,
                "answer": match.instant_answer if mode == "instant" else match.detailed_answer,
                "natural_answer": adapt_answer(match.instant_answer if mode == "instant" else match.detailed_answer) if voice == "natural" else match.instant_answer if mode == "instant" else match.detailed_answer,
                "versions": quick_versions(
                    match.instant_answer if mode == "instant" else match.detailed_answer,
                    adapt_answer(match.instant_answer if mode == "instant" else match.detailed_answer) if voice == "natural" else match.instant_answer if mode == "instant" else match.detailed_answer,
                ),
                "keywords": match.keywords,
                "source_file": match.source_file,
                "memory": relevant_memory(query),
            }
            for match in matches
        ],
    }
