import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QA_DIR = ROOT / "qa_library"
MIN_ALTERNATES = 2
MIN_DETAILED_WORDS = 55


def clean_question(question: str) -> str:
    return re.sub(r"\s+", " ", question.strip().rstrip("?")).strip()


def generated_alternates(question: str) -> list[str]:
    base = clean_question(question)
    lowered = base.lower()
    if lowered.startswith("how do you "):
        action = base[11:]
        return [
            f"Walk me through how you {action}.",
            f"What would you check when you need to {action}?",
        ]
    if lowered.startswith("what is "):
        subject = base[8:]
        return [
            f"Can you explain {subject}?",
            f"How would you describe {subject} in an interview?",
        ]
    if lowered.startswith("what are "):
        subject = base[9:]
        return [
            f"Can you explain {subject}?",
            f"What should I know about {subject}?",
        ]
    if lowered.startswith("explain "):
        subject = base[8:]
        return [
            f"Can you explain {subject}?",
            f"Walk me through {subject}.",
        ]
    return [
        f"Can you walk me through this scenario: {base}?",
        f"What would your approach be for this question: {base}?",
    ]


def ensure_alternates(item: dict) -> bool:
    question = item.get("question") or item.get("scenario") or ""
    if not question:
        return False
    alternates = item.get("alternate_questions") or item.get("alternate_scenarios") or []
    changed = False
    for alternate in generated_alternates(question):
        if len(alternates) >= MIN_ALTERNATES:
            break
        if alternate not in alternates and alternate != question:
            alternates.append(alternate)
            changed = True
    if "alternate_scenarios" in item and "alternate_questions" not in item:
        item["alternate_scenarios"] = alternates
    else:
        item["alternate_questions"] = alternates
    return changed


def ensure_detailed_answer(item: dict) -> bool:
    detailed = item.get("detailed_answer", "")
    if isinstance(detailed, dict):
        text = " ".join(str(value) for value in detailed.values())
    else:
        text = str(detailed)
    if not text.strip():
        structured = item.get("structured_answer", {})
        if isinstance(structured, dict):
            text = " ".join(str(value) for value in structured.values())
    if len(text.split()) >= MIN_DETAILED_WORDS:
        return False

    topic = item.get("topic", "this topic")
    question = item.get("question") or item.get("scenario") or "the question"
    addition = (
        f"\n\nInterview structure:\n"
        f"- Start by answering {question!r} directly.\n"
        f"- Explain the practical checks, examples, and tradeoffs for {topic}.\n"
        f"- Close with how you would validate the result, reduce risk, and prevent the same issue from repeating."
    )
    item["detailed_answer"] = text.rstrip() + addition
    return True


def normalize_file(path: Path) -> tuple[int, int]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        items = payload.get("items", [])
    else:
        items = payload
    if not isinstance(items, list):
        return 0, 0

    alternate_changes = 0
    detail_changes = 0
    for item in items:
        if ensure_alternates(item):
            alternate_changes += 1
        if ensure_detailed_answer(item):
            detail_changes += 1

    if alternate_changes or detail_changes:
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return alternate_changes, detail_changes


def main() -> None:
    total_alternates = 0
    total_details = 0
    for path in sorted(QA_DIR.rglob("*.json")):
        if path.name == "pack_manifest.json":
            continue
        alternate_changes, detail_changes = normalize_file(path)
        total_alternates += alternate_changes
        total_details += detail_changes
        if alternate_changes or detail_changes:
            print(f"{path.relative_to(ROOT)}: alternates={alternate_changes}, details={detail_changes}")
    print(f"Total alternate updates: {total_alternates}")
    print(f"Total detailed-answer updates: {total_details}")


if __name__ == "__main__":
    main()
