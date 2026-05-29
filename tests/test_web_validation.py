import json
import unittest

from app.web import RequestError, parse_answer_request


class WebValidationTests(unittest.TestCase):
    def test_valid_request_defaults(self) -> None:
        request = parse_answer_request(json.dumps({"question": "P1 outage"}))
        self.assertEqual(request["question"], "P1 outage")
        self.assertEqual(request["mode"], "instant")
        self.assertEqual(request["voice"], "natural")
        self.assertEqual(request["limit"], 3)
        self.assertEqual(request["category_filter"], "all")
        self.assertEqual(request["view"], "full")

    def test_empty_question_rejected(self) -> None:
        with self.assertRaises(RequestError):
            parse_answer_request(json.dumps({"question": "   "}))

    def test_bad_limit_rejected(self) -> None:
        with self.assertRaises(RequestError):
            parse_answer_request(json.dumps({"question": "P1 outage", "limit": 99}))

    def test_bad_category_filter_rejected(self) -> None:
        with self.assertRaises(RequestError):
            parse_answer_request(json.dumps({"question": "P1 outage", "category_filter": "bad"}))

    def test_interview_view_accepted(self) -> None:
        request = parse_answer_request(json.dumps({"question": "P1 outage", "view": "interview"}))
        self.assertEqual(request["view"], "interview")

    def test_profession_filter_accepted(self) -> None:
        request = parse_answer_request(json.dumps({"question": "debug API", "category_filter": "developer"}))
        self.assertEqual(request["category_filter"], "developer")


if __name__ == "__main__":
    unittest.main()
