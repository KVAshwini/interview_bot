import tempfile
import unittest
from pathlib import Path

from app import review
from app.review import load_missed_questions


class ReviewTests(unittest.TestCase):
    def test_load_missed_questions_reads_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "missed.jsonl"
            path.write_text('{"query": "unknown question"}\n', encoding="utf-8")
            records = load_missed_questions(path)
        self.assertEqual(records[0]["query"], "unknown question")

    def test_save_review_answer_writes_custom_pack(self) -> None:
        original_dir = review.QA_LIBRARY_DIR
        with tempfile.TemporaryDirectory() as tmpdir:
            review.QA_LIBRARY_DIR = Path(tmpdir)
            try:
                saved = review.save_review_answer("Question?", "Answer.", keywords=["test"])
            finally:
                review.QA_LIBRARY_DIR = original_dir
            self.assertTrue(saved["path"].exists())
            self.assertEqual(saved["item"]["question"], "Question?")


if __name__ == "__main__":
    unittest.main()
