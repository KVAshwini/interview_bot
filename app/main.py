import argparse

from app.answer_engine import answer_payload, find_best_matches, format_match
from app.session_log import log_answer


def main() -> None:
    parser = argparse.ArgumentParser(description="Local interview Q&A helper")
    parser.add_argument("question", nargs="+", help="Question or scenario to answer")
    parser.add_argument("--mode", choices=["instant", "detailed"], default="instant")
    parser.add_argument("--voice", choices=["natural", "raw"], default="natural")
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--no-log", action="store_true", help="Do not save this query to session history")
    args = parser.parse_args()

    query = " ".join(args.question)
    matches = find_best_matches(query, limit=args.limit)
    if not matches:
        print("No local answers found. Generate a new answer and add it to the library.")
        return

    for index, match in enumerate(matches, start=1):
        if index > 1:
            print("\n---\n")
        print(format_match(match, mode=args.mode, voice=args.voice))

    if not args.no_log:
        log_answer(answer_payload(query, mode=args.mode, limit=args.limit, voice=args.voice))


if __name__ == "__main__":
    main()
