import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.answer_engine import find_best_matches


QUERIES = [
    "How do you handle a P1 outage?",
    "AKS pod keeps restarting with crash loop",
    "Kafka lag keeps increasing",
    "Managed identity cannot read Key Vault secret",
    "API is timing out with 504 errors",
    "Tell me about yourself",
]


def main() -> None:
    durations = []
    for query in QUERIES:
        started = time.perf_counter()
        match = find_best_matches(query, limit=1)[0]
        duration_ms = (time.perf_counter() - started) * 1000
        durations.append(duration_ms)
        print(f"{duration_ms:7.2f} ms | {match.score:.2f} | {match.topic} | {query}")
    average = sum(durations) / len(durations)
    print(f"\nAverage: {average:.2f} ms")


if __name__ == "__main__":
    main()
