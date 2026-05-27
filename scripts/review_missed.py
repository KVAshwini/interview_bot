import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.config import OUTPUTS_DIR
from app.review import load_missed_questions


def main() -> None:
    parser = argparse.ArgumentParser(description="Show low-confidence questions captured for review")
    parser.add_argument("--file", help="Optional missed-question JSONL file")
    args = parser.parse_args()

    path = Path(args.file) if args.file else OUTPUTS_DIR / "missed_questions"
    if path.is_dir():
        files = sorted(path.glob("*.jsonl"))
        if not files:
            print("No missed questions captured yet.")
            return
        path = files[-1]

    records = load_missed_questions(path)
    if not records:
        print("No missed questions captured yet.")
        return

    for index, record in enumerate(records, start=1):
        print(f"{index}. {record['query']}")
        print(f"   reason: {record['reason']}")
        for match in record["top_matches"]:
            print(f"   - {match['score']:.2f} {match['topic']} ({match['id']})")
        print()

    print(f"Source: {path}")


if __name__ == "__main__":
    main()
