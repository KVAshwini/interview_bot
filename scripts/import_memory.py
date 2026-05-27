import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY_DIR = ROOT / "memory"


def main() -> None:
    parser = argparse.ArgumentParser(description="Import resume/project notes into local memory")
    parser.add_argument("source", help="Path to a .md, .txt, or .json file")
    parser.add_argument("--name", help="Optional destination filename")
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"File not found: {source}")
    if source.suffix.lower() not in {".md", ".txt", ".json"}:
        raise SystemExit("Only .md, .txt, and .json memory files are supported in this local MVP")

    destination_name = args.name or source.name
    destination = MEMORY_DIR / destination_name
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    print(f"Imported memory file to {destination}")


if __name__ == "__main__":
    main()
