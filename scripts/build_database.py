import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.db import connect, init_db, upsert_items
from app.library_loader import load_library


def main() -> None:
    items = load_library()
    with connect() as conn:
        init_db(conn)
        upsert_items(conn, items)
    print(f"Loaded {len(items)} Q&A items into {ROOT / 'data' / 'interview_library.db'}")


if __name__ == "__main__":
    main()
