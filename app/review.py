import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.config import OUTPUTS_DIR, QA_LIBRARY_DIR


def missed_question_path() -> Path:
    path = OUTPUTS_DIR / "missed_questions" / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def record_missed_question(payload: dict) -> Optional[Path]:
    if not payload.get("needs_review"):
        return None

    path = missed_question_path()
    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "query": payload.get("query", ""),
        "mode": payload.get("mode", "instant"),
        "voice": payload.get("voice", "natural"),
        "reason": payload.get("review_reason", "needs review"),
        "top_matches": [
            {
                "id": match.get("id"),
                "topic": match.get("topic"),
                "score": match.get("score"),
                "question": match.get("question"),
                "source_file": match.get("source_file"),
                "overlap": match.get("explanation", {}).get("overlap", []),
            }
            for match in payload.get("matches", [])[:3]
        ],
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")
    return path


def load_missed_questions(path: Optional[Path] = None) -> list[dict]:
    target = path or missed_question_path()
    if not target.exists():
        return []
    return [
        json.loads(line)
        for line in target.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def load_recent_missed_questions(limit: int = 25) -> list[dict]:
    base = OUTPUTS_DIR / "missed_questions"
    if not base.exists():
        return []
    records: list[dict] = []
    for path in sorted(base.glob("*.jsonl"), reverse=True):
        for record in reversed(load_missed_questions(path)):
            record = dict(record)
            record["source_path"] = str(path)
            records.append(record)
            if len(records) >= limit:
                return records
    return records


def _slug(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return value[:70] or "custom"


def save_review_answer(
    question: str,
    answer: str,
    topic: str = "Custom Review",
    category: str = "custom",
    keywords: Optional[list[str]] = None,
) -> dict:
    question = question.strip()
    answer = answer.strip()
    topic = topic.strip() or "Custom Review"
    category = category.strip() or "custom"
    if not question:
        raise ValueError("question is required")
    if not answer:
        raise ValueError("answer is required")

    path = QA_LIBRARY_DIR / "custom" / "reviewed_questions.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    items = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    item_id = f"review_{datetime.now().strftime('%Y%m%d%H%M%S')}_{_slug(question)[:32]}"
    item = {
        "id": item_id,
        "category": category,
        "topic": topic,
        "question": question,
        "alternate_questions": [],
        "instant_answer": answer,
        "detailed_answer": answer,
        "keywords": keywords or [],
        "answer_style": "reviewed_custom_answer",
        "difficulty": "medium",
    }
    items.append(item)
    path.write_text(json.dumps(items, indent=2) + "\n", encoding="utf-8")
    return {"item": item, "path": path}
