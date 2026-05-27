import tempfile
import unittest
from pathlib import Path

from app.review import load_missed_questions


class ReviewTests(unittest.TestCase):
    def test_load_missed_questions_reads_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "missed.jsonl"
            path.write_text('{"query": "unknown question"}\n', encoding="utf-8")
            records = load_missed_questions(path)
        self.assertEqual(records[0]["query"], "unknown question")


if __name__ == "__main__":
    unittest.main()
