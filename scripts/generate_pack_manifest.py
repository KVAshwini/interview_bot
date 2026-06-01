import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.pack_manager import load_pack_manifest, write_pack_manifest


def main() -> None:
    path = write_pack_manifest()
    manifest = load_pack_manifest()
    print(f"Wrote {manifest['pack_count']} pack records to {path}")
    print(f"Indexed {manifest['total_items']} Q&A items")


if __name__ == "__main__":
    main()
