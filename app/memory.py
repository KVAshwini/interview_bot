import json
from pathlib import Path
from typing import Union

from app.config import MEMORY_DIR
from app.text_utils import similarity


def _read_text(path: Path) -> str:
    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        return json.dumps(payload, indent=2)
    return path.read_text(encoding="utf-8")


def load_memory() -> list[dict[str, str]]:
    memories: list[dict[str, str]] = []
    for path in sorted(MEMORY_DIR.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".txt", ".json"}:
            memories.append(
                {
                    "name": path.stem.replace("_", " ").title(),
                    "path": str(path.relative_to(MEMORY_DIR.parent)),
                    "text": _read_text(path),
                }
            )
    return memories


def relevant_memory(query: str, limit: int = 2) -> list[dict[str, Union[str, float]]]:
    scored = []
    for memory in load_memory():
        score = similarity(query, memory["text"])
        if score > 0.05:
            scored.append({**memory, "score": score})
    return sorted(scored, key=lambda item: item["score"], reverse=True)[:limit]
