import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from app.config import QA_LIBRARY_DIR
from app.library_loader import load_items


MANIFEST_NAME = "pack_manifest.json"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pack_record(path: Path, base_dir: Path = QA_LIBRARY_DIR) -> dict[str, Any]:
    items = load_items(path)
    topics = Counter(str(item.get("topic", "General")) for item in items)
    categories = Counter(str(item.get("category", "general")) for item in items)
    relative = path.relative_to(base_dir)
    return {
        "id": relative.with_suffix("").as_posix().replace("/", "."),
        "name": relative.stem.replace("_", " ").title(),
        "version": "1.0.0",
        "schema_version": 1,
        "path": str(path.relative_to(base_dir.parent)).replace("\\", "/"),
        "item_count": len(items),
        "topics": dict(sorted(topics.items())),
        "categories": dict(sorted(categories.items())),
        "sha256": file_sha256(path),
        "content_only": True,
        "installable": True,
    }


def build_pack_manifest(base_dir: Path = QA_LIBRARY_DIR) -> dict[str, Any]:
    pack_files = [
        path
        for path in sorted(base_dir.rglob("*.json"))
        if path.name != MANIFEST_NAME
    ]
    packs = [pack_record(path, base_dir=base_dir) for path in pack_files]
    return {
        "schema_version": 1,
        "generated_by": "scripts/generate_pack_manifest.py",
        "pack_count": len(packs),
        "total_items": sum(pack["item_count"] for pack in packs),
        "packs": packs,
    }


def write_pack_manifest(base_dir: Path = QA_LIBRARY_DIR) -> Path:
    manifest = build_pack_manifest(base_dir=base_dir)
    path = base_dir / MANIFEST_NAME
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return path


def load_pack_manifest(base_dir: Path = QA_LIBRARY_DIR) -> dict[str, Any]:
    path = base_dir / MANIFEST_NAME
    if not path.exists():
        return build_pack_manifest(base_dir=base_dir)
    return json.loads(path.read_text(encoding="utf-8"))
