import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.config import QA_LIBRARY_DIR


def main() -> None:
    parser = argparse.ArgumentParser(description="Add a question to a JSON Q&A pack")
    parser.add_argument("--pack", required=True, help="Pack path under qa_library, for example scenarios/custom.json")
    parser.add_argument("--id", required=True)
    parser.add_argument("--category", default="custom")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--question", required=True)
    parser.add_argument("--answer", required=True)
    parser.add_argument("--keywords", default="", help="Comma-separated keywords")
    args = parser.parse_args()

    path = QA_LIBRARY_DIR / args.pack
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        items = json.loads(path.read_text(encoding="utf-8"))
    else:
        items = []

    if any(item.get("id") == args.id for item in items):
        raise SystemExit(f"An item with id {args.id} already exists in {path}")

    items.append(
        {
            "id": args.id,
            "category": args.category,
            "topic": args.topic,
            "question": args.question,
            "alternate_questions": [],
            "instant_answer": args.answer,
            "detailed_answer": args.answer,
            "keywords": [keyword.strip() for keyword in args.keywords.split(",") if keyword.strip()],
            "answer_style": "personal cached answer",
            "difficulty": "medium",
        }
    )

    path.write_text(json.dumps(items, indent=2) + "\n", encoding="utf-8")
    print(f"Added {args.id} to {path}")
    print("Run: python3 scripts/build_database.py")


if __name__ == "__main__":
    main()
