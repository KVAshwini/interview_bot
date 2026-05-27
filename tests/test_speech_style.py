import unittest

from app.speech_style import adapt_answer


class SpeechStyleTests(unittest.TestCase):
    def test_adapt_answer_removes_duplicate_i_after_starter(self) -> None:
        answer = "I first check logs and alerts. I keep stakeholders updated."
        natural = adapt_answer(answer)
        self.assertIn("Usually what I do is first check logs", natural)
        self.assertNotIn("is i first", natural.lower())


if __name__ == "__main__":
    unittest.main()
