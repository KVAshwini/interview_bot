import unittest

from app.answer_engine import answer_payload, find_best_matches


class AnswerEngineTests(unittest.TestCase):
    def test_exact_question_matches_p1_outage(self) -> None:
        match = find_best_matches("How do you handle a P1 outage?", limit=1)[0]
        self.assertEqual(match.topic, "Production Incident")
        self.assertGreaterEqual(match.score, 0.85)

    def test_payload_includes_natural_versions(self) -> None:
        payload = answer_payload("How do you handle a P1 outage?", limit=1)
        match = payload["matches"][0]
        self.assertIn("versions", match)
        self.assertIn("Usually what I do is", match["versions"]["natural"])
        self.assertIn("quick", match["versions"])

    def test_payload_marks_low_confidence_for_review(self) -> None:
        payload = answer_payload("completely unrelated fruit salad question", limit=1)
        self.assertTrue(payload["needs_review"])
        self.assertTrue(payload["matches"][0]["explanation"]["needs_review"])


if __name__ == "__main__":
    unittest.main()
