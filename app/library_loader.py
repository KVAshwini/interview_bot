import json
from pathlib import Path
from typing import Any

from app.config import QA_LIBRARY_DIR


def iter_library_files(base_dir: Path = QA_LIBRARY_DIR) -> list[Path]:
    return sorted(path for path in base_dir.rglob("*.json") if path.name != "pack_manifest.json")


def load_items(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("items"), list):
        return payload["items"]
    raise ValueError(f"{path} must contain a list or an object with an items list")


def load_library(base_dir: Path = QA_LIBRARY_DIR) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for path in iter_library_files(base_dir):
        for item in load_items(path):
            item = dict(item)
            item["source_file"] = str(path.relative_to(base_dir.parent))
            items.append(item)
    return items
