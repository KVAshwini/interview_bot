import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.config import OUTPUTS_DIR


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
