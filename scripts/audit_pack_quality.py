import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.library_loader import iter_library_files, load_items


MIN_ALTERNATES = 2
MIN_INSTANT_WORDS = 28
MIN_DETAILED_WORDS = 55
TEMPLATE_PHRASES = [
    "I approach it systematically instead of guessing",
    "the main things I watch are",
    "I explain the immediate action",
]


def word_count(value: str) -> int:
    return len(str(value).split())


def audit_item(item: dict, source: Path) -> list[str]:
    issues = []
    alternates = item.get("alternate_questions") or item.get("alternate_scenarios") or []
    instant = str(item.get("instant_answer", ""))
    detailed = item.get("detailed_answer", "")
    if isinstance(detailed, dict):
        detailed = " ".join(str(value) for value in detailed.values())
    detailed = str(detailed)

    if len(alternates) < MIN_ALTERNATES:
        issues.append("few_alternates")
    if word_count(instant) < MIN_INSTANT_WORDS:
        issues.append("short_instant")
    if word_count(detailed) < MIN_DETAILED_WORDS:
        issues.append("short_detailed")
    if any(phrase in instant or phrase in detailed for phrase in TEMPLATE_PHRASES):
        issues.append("template_style")
    if not item.get("keywords"):
        issues.append("missing_keywords")
    if not item.get("difficulty"):
        issues.append("missing_difficulty")
    return issues


def main() -> None:
    issue_counts: Counter[str] = Counter()
    topic_counts: Counter[str] = Counter()
    examples = []

    for path in iter_library_files():
        for item in load_items(path):
            issues = audit_item(item, path)
            if not issues:
                continue
            topic = str(item.get("topic", "General"))
            topic_counts[topic] += 1
            issue_counts.update(issues)
            if len(examples) < 20:
                examples.append(
                    {
                        "id": item.get("id"),
                        "topic": topic,
                        "question": item.get("question") or item.get("scenario"),
                        "issues": issues,
                        "source": str(path.relative_to(ROOT)),
                    }
                )

    print("Pack quality audit")
    print("==================")
    print(f"Issue counts: {dict(sorted(issue_counts.items()))}")
    print(f"Topics with issues: {dict(topic_counts.most_common(15))}")
    if examples:
        print("\nExamples:")
        for example in examples:
            print(f"- {example['id']} [{', '.join(example['issues'])}] {example['question']} ({example['source']})")


if __name__ == "__main__":
    main()
