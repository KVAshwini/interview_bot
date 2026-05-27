import json
from datetime import datetime
from pathlib import Path

from app.config import OUTPUTS_DIR
from app.review import record_missed_question


def log_answer(payload: dict) -> Path:
    session_dir = OUTPUTS_DIR / "session_transcripts"
    session_dir.mkdir(parents=True, exist_ok=True)
    path = session_dir / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        **payload,
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")
    record_missed_question(payload)
    return path
