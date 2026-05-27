import json
import sqlite3

from app.config import DB_PATH
from app.db import all_items, connect
from app.memory import relevant_memory
from app.models import AnswerMatch
from app.semantic_search import category_boost, semantic_score
from app.speech_style import adapt_answer, quick_versions
from app.text_utils import similarity, token_overlap, tokens


MISS_THRESHOLD = 0.60
ALLOWED_CATEGORY_FILTERS = {"all", "devops", "kubernetes", "azure", "terraform", "linux", "scenario", "behavioral"}


def _matches_category_filter(row: sqlite3.Row, category_filter: str) -> bool:
    if category_filter == "all":
        return True
    haystack = " ".join(
        [
            row["category"],
            row["topic"],
            row["question"],
            row["source_file"],
            row["searchable_text"],
        ]
    ).lower()
    if category_filter == "scenario":
        return row["category"] == "scenarios" or "scenario" in haystack or "production" in haystack
    if category_filter == "behavioral":
        return row["category"] == "behavioral" or "behavioral" in haystack or "hr" in haystack
    if category_filter == "devops":
        return any(term in haystack for term in ["devops", "ci/cd", "pipeline", "deployment", "incident"])
    if category_filter == "kubernetes":
        return any(term in haystack for term in ["kubernetes", "aks", "pod", "ingress", "helm"])
    if category_filter == "azure":
        return any(term in haystack for term in ["azure", "aks", "key vault", "app service"])
    if category_filter == "terraform":
        return "terraform" in haystack or "iac" in haystack
    if category_filter == "linux":
        return "linux" in haystack
    return True


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


def _best_candidate(query: str, row: sqlite3.Row, category_filter: str = "all") -> tuple[float, str]:
    scored = []
    for candidate in _candidate_texts(row):
        lexical = similarity(query, candidate)
        semantic = semantic_score(query, candidate)
        boost = category_boost(category_filter, candidate)
        scored.append((round(min(1.0, (lexical * 0.76) + (semantic * 0.24) + boost), 4), candidate))
    return max(scored, key=lambda item: item[0]) if scored else (0.0, "")


def _best_score(query: str, row: sqlite3.Row, category_filter: str = "all") -> float:
    base = _best_candidate(query, row, category_filter)[0]
    query_tokens = set(tokens(query))
    question_tokens = set(tokens(row["question"]))
    coverage = len(query_tokens & question_tokens) / len(query_tokens) if query_tokens else 0.0
    action_terms = {"handle", "troubleshoot", "debug", "check", "fix", "resolve", "prevent", "monitor"}
    action_boost = 0.04 if query_tokens & action_terms and question_tokens & action_terms else 0.0
    return round(min(1.0, base + (coverage * 0.18) + action_boost), 4)


def find_best_matches(query: str, limit: int = 3, category_filter: str = "all") -> list[AnswerMatch]:
    if category_filter not in ALLOWED_CATEGORY_FILTERS:
        category_filter = "all"
    with connect(DB_PATH) as conn:
        scored = [
            _row_to_match(row, _best_score(query, row, category_filter))
            for row in all_items(conn)
            if _matches_category_filter(row, category_filter)
        ]
    return sorted(scored, key=lambda match: match.score, reverse=True)[:limit]


def selected_answer(match: AnswerMatch, mode: str) -> str:
    return match.detailed_answer if mode == "detailed" else match.instant_answer


def answer_versions(match: AnswerMatch, mode: str, voice: str) -> dict[str, str]:
    answer = selected_answer(match, mode)
    natural = adapt_answer(answer) if voice == "natural" else answer
    return quick_versions(answer, natural)


def match_payload(match: AnswerMatch, query: str, mode: str, voice: str) -> dict:
    versions = answer_versions(match, mode, voice)
    return {
        "id": match.id,
        "category": match.category,
        "topic": match.topic,
        "question": match.question,
        "score": match.score,
        "confidence": match.confidence,
        "answer": selected_answer(match, mode),
        "natural_answer": versions["natural"],
        "versions": versions,
        "keywords": match.keywords,
        "source_file": match.source_file,
        "memory": relevant_memory(query),
        "explanation": {
            "overlap": token_overlap(query, match.question + " " + " ".join(match.keywords)),
            "threshold": MISS_THRESHOLD,
            "needs_review": match.score < MISS_THRESHOLD,
        },
    }


def format_match(match: AnswerMatch, mode: str = "instant", voice: str = "natural") -> str:
    keywords = ", ".join(match.keywords[:8])
    answer = selected_answer(match, mode)
    natural = answer_versions(match, mode, voice)["natural"]
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


def answer_payload(
    query: str,
    mode: str = "instant",
    limit: int = 3,
    voice: str = "natural",
    category_filter: str = "all",
    view: str = "full",
) -> dict:
    if view == "interview":
        limit = 1
    matches = find_best_matches(query, limit=limit, category_filter=category_filter)
    best_score = matches[0].score if matches else 0.0
    return {
        "query": query,
        "mode": mode,
        "voice": voice,
        "category_filter": category_filter,
        "view": view,
        "needs_review": best_score < MISS_THRESHOLD,
        "review_reason": "low confidence match" if best_score < MISS_THRESHOLD else "",
        "matches": [match_payload(match, query, mode, voice) for match in matches],
    }
